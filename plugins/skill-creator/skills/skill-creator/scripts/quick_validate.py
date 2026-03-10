#!/usr/bin/env python3
"""
スキルの簡易バリデーションスクリプト — 最小バージョン
"""

import sys
import os
import re
import yaml
from pathlib import Path

def validate_skill(skill_path):
    """スキルの基本的なバリデーションを行う"""
    skill_path = Path(skill_path)

    # SKILL.mdの存在確認
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.mdが見つかりません"

    # フロントマターの読み込みとバリデーション
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "YAMLフロントマターが見つかりません"

    # フロントマターの抽出
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "フロントマターの形式が不正です"

    frontmatter_text = match.group(1)

    # YAMLフロントマターの解析
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "フロントマターはYAML辞書である必要があります"
    except yaml.YAMLError as e:
        return False, f"フロントマターのYAMLが不正です: {e}"

    # 許可されるプロパティの定義
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}

    # 予期しないプロパティのチェック（metadataのネストされたキーは除外）
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"SKILL.mdフロントマターに予期しないキーがあります: {', '.join(sorted(unexpected_keys))}。"
            f"許可されるプロパティ: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # 必須フィールドのチェック
    if 'name' not in frontmatter:
        return False, "フロントマターに'name'がありません"
    if 'description' not in frontmatter:
        return False, "フロントマターに'description'がありません"

    # 名前のバリデーション
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"nameは文字列である必要があります。取得した型: {type(name).__name__}"
    name = name.strip()
    if name:
        # 命名規則チェック（kebab-case: 小文字とハイフンのみ）
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"名前'{name}'はkebab-case（小文字、数字、ハイフンのみ）である必要があります"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"名前'{name}'はハイフンで開始/終了したり、連続ハイフンを含むことはできません"
        # 名前の長さチェック（仕様上最大64文字）
        if len(name) > 64:
            return False, f"名前が長すぎます（{len(name)}文字）。最大は64文字です。"

    # 説明文のバリデーション
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"descriptionは文字列である必要があります。取得した型: {type(description).__name__}"
    description = description.strip()
    if description:
        # 山括弧のチェック
        if '<' in description or '>' in description:
            return False, "descriptionに山括弧（< または >）を含めることはできません"
        # 説明文の長さチェック（仕様上最大1024文字）
        if len(description) > 1024:
            return False, f"descriptionが長すぎます（{len(description)}文字）。最大は1024文字です。"

    # compatibilityフィールドのバリデーション（オプション）
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"compatibilityは文字列である必要があります。取得した型: {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"compatibilityが長すぎます（{len(compatibility)}文字）。最大は500文字です。"

    return True, "スキルは有効です！"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python quick_validate.py <スキルディレクトリ>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
