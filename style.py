import urllib.parse
OWL = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
       '<defs><linearGradient id="ct" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B7C4FF"/><stop offset="1" stop-color="#7B93FF"/></linearGradient>'
       '<linearGradient id="cl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5B78FF"/><stop offset="1" stop-color="#3550E8"/></linearGradient>'
       '<linearGradient id="cr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3F59EC"/><stop offset="1" stop-color="#2236B8"/></linearGradient></defs>'
       '<path d="M16 2.5 28.5 9.7 16 16.9 3.5 9.7z" fill="url(#ct)"/>'
       '<path d="M3.5 9.7 16 16.9V30L3.5 22.8z" fill="url(#cl)"/>'
       '<path d="M28.5 9.7 16 16.9V30l12.5-7.2z" fill="url(#cr)"/>'
       '<path d="M16 16.9V30M3.5 9.7 16 16.9l12.5-7.2" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width=".9" stroke-linejoin="round"/></svg>')
OWL_URI = "data:image/svg+xml;utf8," + urllib.parse.quote(OWL)

THEMES = {
 "light": dict(bg="#FFFFFF", side="#F7F7F8", line="#E6E6EA", text="#111113", muted="#6B6B74", box="#F6F6F8", hover="#EFEFF2",
               active="#EAEAEE", btn="#0B0B0C", btnink="#FFFFFF", chip="#F1F1F4"),
 "dark":  dict(bg="#0E0E10", side="#141416", line="#2A2A2F", text="#ECECEF", muted="#8E8E97", box="#1A1A1D", hover="#1F1F23",
               active="#27272C", btn="#F2F2F4", btnink="#0B0B0C", chip="#222226"),
}

def css(theme):
    v = ";".join(f"--{k}:{x}" for k, x in THEMES[theme].items())
    return "<style>@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Unbounded:wght@600;800&display=swap');" \
           f":root{{{v}}}" + BASE.replace("__OWL__", OWL_URI) + "</style>"

BASE = """
html,body,.stApp,p,li,label,input,textarea,button,h1,h2,h3,h4,.stMarkdown,[data-testid="stCaptionContainer"]{font-family:'Poppins',system-ui,sans-serif !important}
.stApp{background:var(--bg)}
.stApp,.stApp p,.stApp li,.stApp label,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp [data-testid=stMarkdownContainer],.stApp summary{color:var(--text)}
.stApp [data-testid=stCaptionContainer],.stApp small{color:var(--muted)}
footer,#MainMenu,[data-testid=stMainMenu],[data-testid=stAppDeployButton],[data-testid=stToolbarActions],[data-testid=stDecoration]{display:none !important}
header[data-testid=stHeader]{background:transparent}
[data-testid=stExpandSidebarButton],[data-testid=stSidebarCollapsedControl],[data-testid=stSidebarCollapseButton],[data-testid=collapsedControl]{visibility:visible !important;display:flex !important;color:var(--muted)}
.block-container{max-width:860px;padding-top:.6rem;padding-bottom:9rem}

/* sidebar */
[data-testid=stSidebar]{background:var(--side);border-right:1px solid var(--line)}
[data-testid=stSidebar][aria-expanded=true]{min-width:290px;width:290px}
[data-testid=stSidebar] .block-container,[data-testid=stSidebarUserContent]{padding-top:1rem}
.brand{display:flex;align-items:center;gap:.7rem;margin:.1rem 0 1rem}
.brand svg{width:34px;height:34px;flex:0 0 34px}
.brand span{font-family:'Unbounded','Poppins',sans-serif !important;font-weight:800;font-size:1.12rem;letter-spacing:.01em;text-transform:uppercase;color:var(--text);line-height:1}
.st-key-newchat button{background:var(--btn);color:var(--btnink);border:none;border-radius:999px;height:44px;font-weight:500;width:100%}
.st-key-newchat button *{color:var(--btnink) !important}
.st-key-newchat button:hover{opacity:.88}
[class*="st-key-nav_"] button,[class*="st-key-navact_"] button,[class*="st-key-chat_"] button,[class*="st-key-act_"] button{
  background:transparent;border:none;border-radius:10px;width:100%;justify-content:flex-start;text-align:left;
  font-weight:400;font-size:.88rem;padding:.5rem .75rem;color:var(--text);box-shadow:none}
[class*="st-key-nav_"] button *,[class*="st-key-navact_"] button *,[class*="st-key-chat_"] button *,[class*="st-key-act_"] button *{color:var(--text) !important}
[class*="st-key-chat_"] button p,[class*="st-key-act_"] button p{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
[class*="st-key-nav_"] button:hover,[class*="st-key-chat_"] button:hover{background:var(--hover)}
[class*="st-key-navact_"] button,[class*="st-key-act_"] button{background:var(--active) !important;font-weight:500}
[class*="st-key-del_"] button{background:transparent;border:none;min-height:0;padding:.2rem;box-shadow:none}
[class*="st-key-del_"] button *{color:var(--muted) !important}
[class*="st-key-del_"] button:hover *{color:#E5484D !important}
.side-h{font-size:.74rem;font-weight:500;color:var(--muted);margin:1.1rem 0 .3rem .4rem}
.empty{color:var(--muted);font-size:.82rem;padding:.2rem .4rem}
.who{display:flex;align-items:center;gap:.7rem;margin-top:1.4rem;padding:.9rem .4rem 0;border-top:1px solid var(--line)}
.who i{width:36px;height:36px;border-radius:50%;background:#C8441B;color:#fff;font-style:normal;display:flex;align-items:center;justify-content:center;font-weight:600}
.who b{display:block;font-size:.88rem;font-weight:500;color:var(--text)}.who small{font-size:.72rem;color:var(--muted)}

/* top bar */
.ttl{text-align:center;font-weight:500;font-size:.95rem;padding-top:.55rem;color:var(--text)}
[class*="st-key-tb_"] button,[class*="st-key-tba_"] button{border:none;background:transparent;border-radius:10px;min-height:0;height:36px;width:36px;padding:0;box-shadow:none}
[class*="st-key-tb_"] button *,[class*="st-key-tba_"] button *{color:var(--muted) !important}
[class*="st-key-tb_"] button:hover{background:var(--hover)}
[class*="st-key-tba_"] button{background:var(--active)}
[class*="st-key-tba_"] button *{color:var(--text) !important}
.st-key-settings [data-testid=stPopover]>div>button{border:none;background:transparent;height:36px;width:36px;padding:0}
.st-key-settings [data-testid=stPopover] button *{color:var(--muted) !important}
.topline{border-bottom:1px solid var(--line);margin:.2rem -1rem 0}

/* hero + chips */
.hero{text-align:center;margin:15vh 0 1.8rem}
.hero svg{width:60px;height:60px}
.hero .t{font-size:1.6rem;font-weight:600;margin-top:1rem;color:var(--text)}
.hero .s{color:var(--muted);font-weight:300;font-size:.92rem;margin-top:.35rem}
.stApp .stButton>button{border:1px solid var(--line);border-radius:999px;background:var(--bg);font-weight:400;font-size:.84rem;padding:.5rem 1rem;height:auto;box-shadow:none;transition:all .15s}
.stApp .stButton>button *{color:var(--text) !important}
.stApp .stButton>button:hover{background:var(--hover);border-color:var(--muted)}
.stApp .stButton>button p{white-space:normal}

/* cards */
.card{border:1px solid var(--line);border-radius:14px;background:var(--box);padding:.9rem 1.1rem;margin:.5rem 0}
.card b{font-weight:500;color:var(--text)}.card span{color:var(--muted);font-size:.8rem}
.card .q{color:var(--muted);font-size:.82rem;margin-bottom:.35rem}
h3.pg{font-size:1.25rem;font-weight:600;margin:1.2rem 0 .2rem;color:var(--text)}
p.pgs{color:var(--muted);font-size:.9rem;font-weight:300;margin-bottom:1rem}
.tchip{display:inline-block;padding:.3rem .85rem;margin:.2rem .35rem .2rem 0;border-radius:999px;background:var(--chip);color:var(--text);font-size:.82rem}

/* inputs / widgets in both themes */
.stApp [data-baseweb=select]>div{background:var(--box) !important;border-color:var(--line) !important;color:var(--text) !important}
.stApp [data-baseweb=select] *{color:var(--text) !important;fill:var(--muted) !important}
[data-baseweb=popover] [data-baseweb=menu],[data-baseweb=popover] ul{background:var(--bg) !important}
[data-baseweb=popover] li{color:var(--text) !important;background:transparent !important}
[data-baseweb=popover] li:hover{background:var(--hover) !important}
[data-testid=stPopoverBody]{background:var(--bg) !important;border:1px solid var(--line) !important}
[data-testid=stFileUploaderDropzone]{background:var(--box);border:1px dashed var(--line);border-radius:14px}
[data-testid=stFileUploaderDropzone] *{color:var(--muted) !important}
[data-testid=stFileUploaderDropzone] button{background:var(--bg) !important;border:1px solid var(--line) !important}
[data-testid=stFileUploaderDropzone] button *{color:var(--text) !important}
[data-testid=stFileUploaderFile] *{color:var(--text) !important}
[data-testid=stExpander]{border:1px solid var(--line);border-radius:14px;background:transparent}
[data-testid=stSpinner] *{color:var(--muted) !important}
[data-testid=stToast]{background:var(--bg);border:1px solid var(--line)}

/* messages */
[data-testid=stChatMessageAvatarUser],[data-testid=stChatMessageAvatarAssistant]{display:none}
[data-testid=stChatMessage]{background:transparent;padding:.55rem 0}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarUser]){flex-direction:row-reverse}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarUser]) [data-testid=stChatMessageContent]{background:var(--box);border:1px solid var(--line);border-radius:18px;padding:.7rem 1.1rem;max-width:80%;margin-left:auto}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarAssistant])::before{content:"";flex:0 0 30px;height:30px;margin-right:.8rem;margin-top:.1rem;background:url("__OWL__") no-repeat center/contain}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarAssistant]) [data-testid=stChatMessageContent]{line-height:1.75}
.chip{display:inline-block;padding:.2rem .7rem;margin:.15rem .3rem .15rem 0;border:1px solid var(--line);border-radius:999px;color:var(--muted);font-size:.75rem}
.pass{border-left:2px solid var(--line);padding:.1rem 0 .1rem .8rem;margin:.55rem 0;font-size:.82rem;color:var(--muted);font-weight:300}
.pass b{color:var(--text);font-weight:500}
[class*="st-key-bm_"] button{border:none !important;background:transparent !important;height:30px;min-height:0;width:30px;padding:0}
[class*="st-key-bm_"] button *{color:var(--muted) !important}
[class*="st-key-bmon_"] button *{color:#F5A524 !important}

/* composer */
.st-key-cmp{position:fixed;bottom:1rem;left:calc((100vw + 290px)/2);transform:translateX(-50%);width:min(780px,calc(100vw - 290px - 3rem));z-index:99;
  background:linear-gradient(transparent,var(--bg) 24%);padding-top:1.4rem}
.stApp:has([data-testid=stSidebar][aria-expanded=false]) .st-key-cmp{left:50%;width:min(780px,calc(100vw - 3rem))}
.st-key-cmp [data-testid=stForm]{background:var(--box);border:1px solid var(--line);border-radius:999px;padding:.3rem .5rem .3rem 3.1rem;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.st-key-cmp [data-testid=stForm]:focus-within{border-color:var(--muted)}
.st-key-cmp input{background:transparent !important;border:none !important;box-shadow:none !important;font-size:.98rem;color:var(--text) !important}
.st-key-cmp input::placeholder{color:var(--muted) !important}
.st-key-cmp [data-testid=stTextInputRootElement],.st-key-cmp [data-testid=stTextInput]>div{background:transparent !important;border:none !important;box-shadow:none !important}
[data-testid=InputInstructions]{display:none}
.st-key-cmp [data-testid=stFormSubmitButton] button{background:var(--btn) !important;border:none;border-radius:50%;width:40px;height:40px;min-height:0;padding:0;float:right}
.st-key-cmp [data-testid=stFormSubmitButton] button *{color:var(--btnink) !important}
.st-key-cmp [data-testid=stPopover]{position:absolute;left:.75rem;top:1.75rem;width:auto;z-index:5}
.st-key-cmp [data-testid=stPopover]>div>button{border:none;background:transparent;width:40px;height:40px;padding:0;min-height:0}
.st-key-cmp [data-testid=stPopover] button *{color:var(--muted) !important}
.st-key-cmp [data-testid=stPopover] button [data-testid=stIconMaterial]:last-child:not(:first-child){display:none}
.note{text-align:center;color:var(--muted);font-size:.72rem;margin-top:.45rem}
"""
