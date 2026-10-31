#!/bin/bash
set -euo pipefail

# ===== 配置 =====
CONDA_ENV="aiagent"
COMMIT_MSG="update webpage"
BAK_DIR="../bak"
# ==============================

# 脚本所在目录
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "${SCRIPT_DIR}" || exit 1
echo "✅ 当前工作目录: ${SCRIPT_DIR}"

# 1. git pull origin main
echo -e "\n===== 1/7 git pull origin main ====="
git pull origin main

# 2 & 3 直接用 conda run 执行python，不需要 conda activate
echo -e "\n===== 2/7 在aiagent环境执行 python md2html.py README.md ====="
conda run -n "${CONDA_ENV}" python md2html.py "README.md"

# 4. 复制 index.html 到 ../bak，带日期
echo -e "\n===== 3/7 备份 index.html 到 ${BAK_DIR} ====="
TODAY=$(date +%Y.%m.%d)
mkdir -p "${BAK_DIR}"
if [[ -f "index.html" ]]; then
    cp index.html "${BAK_DIR}/index-${TODAY}.html"
    echo "✅ 备份完成：${BAK_DIR}/index-${TODAY}.html"
else
    echo "❌ 没有生成 index.html，终止脚本"
    exit 1
fi

# 5. git add index.html
echo -e "\n===== 4/7 git add index.html ====="
git add index.html

# 6. git commit
echo -e "\n===== 5/7 git commit -m '${COMMIT_MSG}' ====="
if git diff --cached --quiet; then
    echo "ℹ️ index.html 没有变化，不执行commit和push"
else
    git commit -m "${COMMIT_MSG}"
    # 7. git push
    echo -e "\n===== 6/7 git push origin main ====="
    git push origin main
fi

echo -e "\n🎉 全部任务执行完毕！"
