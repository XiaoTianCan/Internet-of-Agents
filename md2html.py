# -*- coding: utf-8 -*-
import markdown
import os
import argparse
from pathlib import Path
import re
from datetime import datetime

# 生成学术风格的HTML页面
def md_to_academic_html(md_file_path, output_dir=None, title=None, update_date=None):
    """
    将Markdown文件转换为学术风格的HTML文件
    兼容所有版本markdown库，无需依赖FencedCodeBlockPreprocessor
    
    参数：
    md_file_path: str - MD文件路径
    output_dir: str - HTML输出目录（默认与MD文件同目录）
    title: str - HTML页面标题（默认使用MD文件名）
    update_date: str - 更新日期（格式：YYYY-MM-DD，默认使用当前日期）
    """
    # 处理文件路径
    md_file = Path(md_file_path)
    if not md_file.exists():
        raise FileNotFoundError(f"未找到文件：{md_file_path}")
    
    # 确定输出目录和文件名
    if output_dir is None:
        output_dir = md_file.parent
    else:
        os.makedirs(output_dir, exist_ok=True)
    
    html_filename = md_file.stem + '.html'
    html_file = Path(output_dir) / html_filename
    
    # 默认标题使用文件名（去除扩展名）
    if title is None:
        title = md_file.stem.replace('_', ' ').replace('-', ' ').title()
    
    # 默认日期使用当前日期
    if update_date is None:
        update_date = datetime.now().strftime('%Y-%m-%d')
    
    # 读取MD内容
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 配置Markdown解析器（启用常用扩展，使用官方codehilite实现代码高亮）
    md_extensions = [
        'tables',          # 表格支持
        'fenced_code',     # 代码块支持（官方原生）
        'codehilite',      # 代码高亮（适配pygments，官方扩展）
        'nl2br',           # 换行符转换
        'toc',             # 目录生成
        'attr_list',       # 属性列表
        'def_list',        # 定义列表
        'footnotes',       # 脚注
    ]
    
    # 扩展配置：启用代码高亮、行号等
    extension_configs = {
        'toc': {'title': '目录'},
        'codehilite': {
            'linenums': False,        # 不显示行号（如需显示改为True）
            'guess_lang': True,       # 自动识别编程语言
            'css_class': 'codehilite' # 统一代码块样式类名
        }
    }
    
    # 转换MD为HTML内容
    html_content = markdown.markdown(
        md_content,
        extensions=md_extensions,
        extension_configs=extension_configs
    )
    
    # 学术风格的CSS样式（包含代码高亮样式）
    academic_css = """
/* 全局样式 - 学术风格基础 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Times New Roman', Times, serif, 'SimSun', 'Microsoft YaHei';
    font-size: 16px;
    line-height: 1.6;  /* 学术文档最佳行高 */
    color: #333;
    background-color: #f9f9f9;
    max-width: 900px;  /* 学术文档最佳宽度 */
    margin: 0 auto;
    padding: 40px 20px;
}

/* 标题样式 */
h1, h2, h3, h4, h5, h6 {
    font-weight: normal;
    color: #222;
    margin-top: 1.8em;
    margin-bottom: 0.8em;
    border-bottom: none;
}

h1 {
    font-size: 2.2em;
    border-bottom: 2px solid #333;
    padding-bottom: 0.3em;
    margin-top: 0;
}

h2 {
    font-size: 1.8em;
    border-bottom: 1px solid #666;
    padding-bottom: 0.2em;
}

h3 { font-size: 1.5em; }
h4 { font-size: 1.3em; }
h5 { font-size: 1.1em; }
h6 { font-size: 1em; color: #666; }

/* 段落样式 */
p {
    margin-bottom: 1em;
    text-align: justify;  /* 两端对齐，学术风格 */
}

/* 列表样式 */
ul, ol {
    margin: 1em 0;
    padding-left: 2em;
}

li {
    margin-bottom: 0.5em;
}

/* 学术风格表格（三线表） */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1.5em 0;
    font-size: 0.95em;
}

/* 三线表核心样式：仅显示上、下、表头下边框 */
table thead {
    border-bottom: 2px solid #333;
}

table tbody {
    border-bottom: 1px solid #333;
}

th, td {
    padding: 8px 12px;
    text-align: left;
    border: none;  /* 去除默认边框 */
}

th {
    font-weight: bold;
    background-color: #f0f0f0;
}

/* 隔行变色（可选，增强可读性） */
tr:nth-child(even) td {
    background-color: #f8f8f8;
}

/* 代码块样式（适配codehilite扩展） */
.codehilite {
    background-color: #f5f5f5;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 1em;
    margin: 1.5em 0;
    overflow-x: auto;
}

.codehilite pre {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 0.9em;
    line-height: 1.5;
    margin: 0;
    padding: 0;
}

/* 行内代码样式 */
code {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    background-color: #f0f0f0;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 0.9em;
}

/* 链接样式 */
a {
    color: #0066cc;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* 引用样式 */
blockquote {
    border-left: 4px solid #666;
    padding: 0.5em 1em;
    margin: 1em 0;
    background-color: #f5f5f5;
    font-style: italic;
}

/* 图片样式 */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1.5em auto;
    border: 1px solid #ddd;
    padding: 5px;
}

/* 目录样式 */
div.toc {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    padding: 1em;
    margin: 1em 0 2em 0;
    border-radius: 4px;
}

div.toc h2 {
    font-size: 1.3em;
    border-bottom: 1px solid #ccc;
    margin-top: 0;
    margin-bottom: 0.8em;
    padding-bottom: 0.2em;
}

div.toc ul {
    list-style: none;
    padding-left: 1em;
}

div.toc li {
    margin-bottom: 0.3em;
}

/* 脚注样式 */
.footnote {
    font-size: 0.9em;
    color: #666;
}

/* 响应式适配 */
@media (max-width: 768px) {
    body {
        padding: 20px 10px;
        font-size: 15px;
    }
    
    h1 { font-size: 1.8em; }
    h2 { font-size: 1.5em; }
    h3 { font-size: 1.3em; }
}

/* 代码高亮补充样式（适配pygments默认主题） */
.codehilite .hll { background-color: #ffffcc }
.codehilite .c { color: #408080; font-style: italic } /* Comment */
.codehilite .err { border: 1px solid #FF0000 } /* Error */
.codehilite .k { color: #008000; font-weight: bold } /* Keyword */
.codehilite .o { color: #666666 } /* Operator */
.codehilite .ch { color: #408080; font-style: italic } /* Comment.Hashbang */
.codehilite .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.codehilite .cp { color: #BC7A00 } /* Comment.Preproc */
.codehilite .cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
.codehilite .c1 { color: #408080; font-style: italic } /* Comment.Single */
.codehilite .cs { color: #408080; font-style: italic } /* Comment.Special */
.codehilite .gd { color: #A00000 } /* Generic.Deleted */
.codehilite .ge { font-style: italic } /* Generic.Emph */
.codehilite .gr { color: #FF0000 } /* Generic.Error */
.codehilite .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.codehilite .gi { color: #00A000 } /* Generic.Inserted */
.codehilite .go { color: #888888 } /* Generic.Output */
.codehilite .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.codehilite .gt { color: #0044DD } /* Generic.Traceback */
.codehilite .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.codehilite .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.codehilite .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.codehilite .kp { color: #008000 } /* Keyword.Pseudo */
.codehilite .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.codehilite .kt { color: #B00040 } /* Keyword.Type */
.codehilite .m { color: #666666 } /* Literal.Number */
.codehilite .s { color: #BA2121 } /* Literal.String */
.codehilite .na { color: #7D9029 } /* Name.Attribute */
.codehilite .nb { color: #008000 } /* Name.Builtin */
.codehilite .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.codehilite .no { color: #880000 } /* Name.Constant */
.codehilite .nd { color: #AA22FF } /* Name.Decorator */
.codehilite .ni { color: #999999; font-weight: bold } /* Name.Entity */
.codehilite .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.codehilite .nf { color: #0000FF } /* Name.Function */
.codehilite .nl { color: #A0A000 } /* Name.Label */
.codehilite .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.codehilite .nt { color: #008000; font-weight: bold } /* Name.Tag */
.codehilite .nv { color: #19177C } /* Name.Variable */
.codehilite .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.codehilite .w { color: #bbbbbb } /* Text.Whitespace */
.codehilite .mb { color: #666666 } /* Literal.Number.Bin */
.codehilite .mf { color: #666666 } /* Literal.Number.Float */
.codehilite .mh { color: #666666 } /* Literal.Number.Hex */
.codehilite .mi { color: #666666 } /* Literal.Number.Integer */
.codehilite .mo { color: #666666 } /* Literal.Number.Oct */
.codehilite .sa { color: #BA2121 } /* Literal.String.Affix */
.codehilite .sb { color: #BA2121 } /* Literal.String.Backtick */
.codehilite .sc { color: #BA2121 } /* Literal.String.Char */
.codehilite .dl { color: #BA2121 } /* Literal.String.Delimiter */
.codehilite .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.codehilite .s2 { color: #BA2121 } /* Literal.String.Double */
.codehilite .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.codehilite .sh { color: #BA2121 } /* Literal.String.Heredoc */
.codehilite .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.codehilite .sx { color: #008000 } /* Literal.String.Other */
.codehilite .sr { color: #BB6688 } /* Literal.String.Regex */
.codehilite .s1 { color: #BA2121 } /* Literal.String.Single */
.codehilite .ss { color: #19177C } /* Literal.String.Symbol */
.codehilite .bp { color: #008000 } /* Name.Builtin.Pseudo */
.codehilite .fm { color: #0000FF } /* Name.Function.Magic */
.codehilite .vc { color: #19177C } /* Name.Variable.Class */
.codehilite .vg { color: #19177C } /* Name.Variable.Global */
.codehilite .vi { color: #19177C } /* Name.Variable.Instance */
.codehilite .vm { color: #19177C } /* Name.Variable.Magic */
.codehilite .il { color: #666666 } /* Literal.Number.Integer.Long */
    """
    
    # 完整的HTML模板
    full_html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/svg+xml" href="vite.png" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {academic_css}
    </style>
</head>
<body>
    {html_content}
    
    <!-- 页脚信息 -->
    <footer style="margin-top: 3em; padding-top: 1em; border-top: 1px solid #ccc; font-size: 0.9em; color: #666; text-align: center;">
        <a href="https://github.com/XiaoTianCan/Internet-of-Agents">Github Repo</a>  Update Date: {update_date}
    </footer>
</body>
</html>
    """
    
    # 写入HTML文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ 转换完成！HTML文件已保存至：{html_file.absolute()}")
    return str(html_file.absolute())

# 批量转换目录下的所有MD文件
def batch_convert_md_files(input_dir, output_dir=None, update_date=None):
    """批量转换指定目录下的所有.md文件"""
    input_path = Path(input_dir)
    if not input_path.is_dir():
        raise NotADirectoryError(f"输入路径不是目录：{input_dir}")
    
    # 遍历所有MD文件
    md_files = list(input_path.glob('*.md'))
    if not md_files:
        print(f"⚠️ 目录 {input_dir} 中未找到.md文件")
        return
    
    print(f"📁 找到 {len(md_files)} 个MD文件，开始批量转换...")
    for md_file in md_files:
        try:
            md_to_academic_html(str(md_file), output_dir, None, update_date)
        except Exception as e:
            print(f"❌ 转换 {md_file.name} 失败：{str(e)}")

# 命令行交互入口
if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='将Markdown文件转换为学术风格的HTML文件')
    parser.add_argument('path', help='MD文件路径或包含MD文件的目录路径')
    parser.add_argument('-o', '--output', default='./', help='HTML输出目录（可选）')
    parser.add_argument('-t', '--title', default='Internet of Agents', help='HTML页面标题（仅单文件转换时有效）')
    parser.add_argument('-d', '--date', default=datetime.now().strftime('%Y-%m-%d'), help='更新日期（格式：YYYY-MM-DD，默认为当前日期）')
    
    args = parser.parse_args()

    # 判断输入路径是文件还是目录
    input_path = Path(args.path)
    if input_path.is_file():
        # 单文件转换
        md_to_academic_html(args.path, args.output, args.title, args.date)
    elif input_path.is_dir():
        # 批量转换目录下的MD文件
        batch_convert_md_files(args.path, args.output, args.date)
    else:
        print(f"❌ 无效的路径：{args.path}")