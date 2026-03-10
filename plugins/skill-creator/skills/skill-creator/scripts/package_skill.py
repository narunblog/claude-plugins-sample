#!/usr/bin/env python3
"""
スキルパッケージャー — スキルフォルダから配布可能な.skillファイルを作成する

使用方法:
    python utils/package_skill.py <path/to/skill-folder> [output-directory]

例:
    python utils/package_skill.py skills/public/my-skill
    python utils/package_skill.py skills/public/my-skill ./dist
"""

import fnmatch
import sys
import zipfile
from pathlib import Path
from scripts.quick_validate import validate_skill

# パッケージング時に除外するパターン
EXCLUDE_DIRS = {"__pycache__", "node_modules"}
EXCLUDE_GLOBS = {"*.pyc"}
EXCLUDE_FILES = {".DS_Store"}
# スキルルートでのみ除外されるディレクトリ（ネストされた場合は除外しない）
ROOT_EXCLUDE_DIRS = {"evals"}


def should_exclude(rel_path: Path) -> bool:
    """パスがパッケージングから除外されるべきかチェックする。"""
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    # rel_pathはskill_path.parentからの相対パス。parts[0]がスキルフォルダ名、
    # parts[1]（存在する場合）が最初のサブディレクトリ。
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    name = rel_path.name
    if name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_GLOBS)


def package_skill(skill_path, output_dir=None):
    """
    スキルフォルダを.skillファイルにパッケージングする。

    引数:
        skill_path: スキルフォルダへのパス
        output_dir: .skillファイルの出力先ディレクトリ（省略時はカレントディレクトリ）

    戻り値:
        作成された.skillファイルへのパス、またはエラー時はNone
    """
    skill_path = Path(skill_path).resolve()

    # スキルフォルダの存在確認
    if not skill_path.exists():
        print(f"❌ エラー: スキルフォルダが見つかりません: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ エラー: パスがディレクトリではありません: {skill_path}")
        return None

    # SKILL.mdの存在確認
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ エラー: SKILL.mdが見つかりません: {skill_path}")
        return None

    # パッケージング前にバリデーション実行
    print("🔍 スキルをバリデーション中...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ バリデーション失敗: {message}")
        print("   パッケージング前にバリデーションエラーを修正してください。")
        return None
    print(f"✅ {message}\n")

    # 出力先の決定
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    # .skillファイル（ZIP形式）の作成
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # ビルド成果物を除外しながらスキルディレクトリを走査
            for file_path in skill_path.rglob('*'):
                if not file_path.is_file():
                    continue
                arcname = file_path.relative_to(skill_path.parent)
                if should_exclude(arcname):
                    print(f"  スキップ: {arcname}")
                    continue
                zipf.write(file_path, arcname)
                print(f"  追加: {arcname}")

        print(f"\n✅ スキルのパッケージングに成功しました: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"❌ .skillファイルの作成中にエラー: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("使用方法: python utils/package_skill.py <path/to/skill-folder> [output-directory]")
        print("\n例:")
        print("  python utils/package_skill.py skills/public/my-skill")
        print("  python utils/package_skill.py skills/public/my-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 スキルをパッケージング中: {skill_path}")
    if output_dir:
        print(f"   出力ディレクトリ: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
