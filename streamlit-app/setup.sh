mkdir -p ~/.streamlit/

echo "\
[theme]\n\
primaryColor = '#648fd1'\n\
backgroundColor = '#f0f0f5'\n\
secondaryBackgroundColor = '#e0e0ef'\n\
textColor= '#262730'\n\
font = 'sans serif'\n\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml