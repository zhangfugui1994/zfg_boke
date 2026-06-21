import re, json

dir_path = r'E:\workspace\网站\商品目录'
md_files = sorted([f for f in __import__('os').listdir(dir_path) if f.endswith('.md')])

colors = ['FF6B6B','4ECDC4','45B7D1','96CEB4','FFEAA7','DDA0DD','98D8C8','F7DC6F','BB8FCE','85C1E9']

posts = []
for idx, filename in enumerate(md_files):
    filepath = __import__('os').path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fm_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    body = fm_match.group(2) if fm_match else content

    # 提取分享链接
    share_link = ''
    if fm_match:
        link_match = re.search(r'share_link:\s*(.+)', fm_match.group(1))
        if link_match: share_link = link_match.group(1).strip()

    # 提取标题
    title_match = re.match(r'#\s+(.+)', body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "无标题"

    # 提取大小
    size_match = re.search(r'【全([\d.]+[GMKBT]?)】', title)
    if not size_match: size_match = re.search(r'【全([\d.]+[GMKBT]?)】', body)
    size = size_match.group(1) if size_match else ""

    # 提取评分（支持前后空格）
    looks = re.search(r'颜值[\s：]*([\d.]+)', body)
    figure = re.search(r'身材[\s：]*([\d.]+)', body)
    rarity = re.search(r'稀缺度[\s：]*(\w+)', body)

    looks = looks.group(1) if looks else "0"
    figure = figure.group(1) if figure else "0"
    rarity = rarity.group(1) if rarity else ""

    # 提取分享更新时间
    updated = ""
    if fm_match:
        updated_match = re.search(r'share_updated:\s*(.+)', fm_match.group(1))
        if updated_match: updated = updated_match.group(1).strip()

    # 提取封面图片
    cover_image = ""
    img_match = re.search(r'!\[.*?\]\(([^)]+)\)', body)
    if img_match:
        img_path = img_match.group(1).strip()
        if '/预览/' in img_path:
            cover_image = img_path.split('/预览/')[-1]
        elif '/' in img_path:
            cover_image = img_path
        else:
            cover_image = img_path

    name_for_cover = filename.replace('.md', '').split('.', 1)[-1]
    color = colors[idx % len(colors)]
    placeholder_url = f'https://via.placeholder.com/400x440/{color}/FFFFFF?text={name_for_cover[:4]}'

    post = {
        "title": title,
        "subtitle": f"颜值:{looks} | 身材:{figure} | 稀缺度:{rarity}",
        "size": size,
        "cover_image": placeholder_url,
        "cover_local": cover_image,
        "share_link": share_link,
        "name": name_for_cover,
        "updated": updated
    }
    posts.append(post)

with open(__import__('os').path.join(dir_path, '..', '商品目录.json'), 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print(f'Done: {len(posts)} products')
for p in posts:
    print(f'  {p["name"]}: {p["subtitle"]}')
