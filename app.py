import streamlit as st
import html
import re

st.set_page_config(page_title="Post Generator", layout="wide")
st.title("📝 Post Generator – Galileo Template")

st.markdown("""
Chào bạn! Hãy điền các thông tin bên dưới để tạo bài viết HTML cho template Galileo.  
- Hỗ trợ Markdown với `# ## ### ####` và đánh số tự động.  
- Chèn ảnh bonus giữa các đoạn với cú pháp: `![alt text](path/to/image.jpg)`  
""")

# -------------------------------
# Nhập liệu
# -------------------------------
with st.expander("Thông tin bài viết", expanded=True):
    title = st.text_input("Tiêu đề chính (H1)")
    subtitle = st.text_input("Phụ đề / dòng 2 của tiêu đề (tuỳ chọn)")
    author = st.text_input("Tác giả")
    image = st.text_input("Ảnh chính trong bài (URL hoặc path)", "images/sample.jpg")

with st.expander("Nội dung bài viết (Markdown)"):
    content = st.text_area(
        "Nội dung (Markdown, hỗ trợ # ## ### ####, và ![alt](path) cho ảnh bonus)",
        height=400
    )

# -------------------------------
# Hàm convert Markdown -> HTML
# -------------------------------
def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out = []

    h1_counter = 0
    h2_counter = 0
    h3_counter = 0
    h4_counter = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Kiểm tra ảnh bonus
        img_match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
        if img_match:
            alt_text = img_match.group(1)
            img_path = img_match.group(2)
            out.append(f'<img src="{html.escape(img_path)}" class="post-image" alt="{html.escape(alt_text)}">')
            continue

        if line.startswith("#### "):
            h4_counter += 1
            html_line = f"<h4>{h1_counter}.{h2_counter}.{h3_counter}.{h4_counter} {html.escape(line[5:])}</h4>"
            out.append(html_line)
        elif line.startswith("### "):
            h3_counter += 1
            h4_counter = 0
            html_line = f"<h3>{h1_counter}.{h2_counter}.{h3_counter} {html.escape(line[4:])}</h3>"
            out.append(html_line)
        elif line.startswith("## "):
            h2_counter += 1
            h3_counter = 0
            h4_counter = 0
            html_line = f"<h2>{h1_counter}.{h2_counter} {html.escape(line[3:])}</h2>"
            out.append(html_line)
        elif line.startswith("# "):
            h1_counter += 1
            h2_counter = 0
            h3_counter = 0
            h4_counter = 0
            html_line = f"<h2>{h1_counter} {html.escape(line[2:])}</h2>"  # H1 chính dùng title
            out.append(html_line)
        else:
            out.append(f"<p>{html.escape(line)}</p>")

    return "\n".join(out)

# -------------------------------
# Tạo phần main HTML
# -------------------------------
def generate_main(title, subtitle, author, image, content_html):
    full_title = html.escape(title)
    if subtitle:
        full_title += "<br>" + html.escape(subtitle)

    return f"""
  <!-- Hero cho trang con -->
  <section class="post-title">
    <div class="container">
      <h1>{full_title}</h1>
      <h2 class="lead">{html.escape(author)}</h2>
    </div>
  </section>

  <!-- Nội dung chính -->
  <main class="section">
    <div class="container">
      <article class="post-content">
        <img src="{html.escape(image)}" class="post-image" alt="">
        {content_html}
      </article>
    </div>
  </main>
"""

# -------------------------------
# Xuất HTML
# -------------------------------
if st.button("📥 Xuất HTML"):
    if not title or not author or not content:
        st.warning("Vui lòng điền ít nhất: tiêu đề, tác giả, nội dung.")
    else:
        content_html = md_to_html(content)
        new_main = generate_main(title, subtitle, author, image, content_html)

        # Đọc template gốc
        try:
            with open("template.html", encoding="utf-8") as f:
                tpl = f.read()
        except FileNotFoundError:
            st.error("Không tìm thấy file template.html. Vui lòng đặt cùng folder.")
            st.stop()

        # Thay thế khối Hero + Main
        final_html = re.sub(
            r"<!-- Hero cho trang con -->.*?<!-- Nội dung chính -->.*?</main>",
            new_main.strip(),
            tpl,
            flags=re.S
        )

        st.download_button(
            "📥 Tải file HTML",
            final_html,
            file_name="post.html",
            mime="text/html"
        )
        st.success("✅ Đã tạo xong post.html với header/footer y nguyên, chỉ thay main.")
