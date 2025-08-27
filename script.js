document.addEventListener("DOMContentLoaded", () => {
  fetch("posts.json")
    .then(res => res.json())
    .then(data => {
      // sort theo ngày mới nhất
      data.sort((a, b) => new Date(b.date) - new Date(a.date));

      const container = document.getElementById("posts-container");
      container.innerHTML = `
        <div class="container">
          <h2 class="section-title text-center">BÀI VIẾT MỚI NHẤT</h2>
          <div class="posts-grid"></div>
          <div class="text-center mt-6">
            <a href="articles.html" class="btn btn-primary">TÌM HIỂU THÊM</a>
          </div>
        </div>
      `;

      const grid = container.querySelector(".posts-grid");

      data.forEach(post => {
        const card = document.createElement("div");
        card.className = "post-card";

        card.innerHTML = `
          <div class="post-thumb">
            <a href="${post.link}">
              <img src="${post.image || 'images/default.jpg'}" alt="${post.title}">
            </a>
          </div>
          <div class="post-info">
            <p class="post-date">${new Date(post.date).toLocaleDateString("vi-VN")}</p>
            <h3 class="post-title">
              <a href="${post.link}">${post.title}</a>
            </h3>
          </div>
        `;

        grid.appendChild(card);
      });
    })
    .catch(err => console.error("Error loading posts:", err));
});
function loadPosts(jsonFile, limit = null) {
  fetch(jsonFile)
    .then(res => res.json())
    .then(data => {
      data.sort((a, b) => new Date(b.date) - new Date(a.date));

      const container = document.getElementById("posts-container");
      container.innerHTML = `
        <div class="container">
          <h2 class="section-title text-center">BÀI VIẾT MỚI NHẤT</h2>
          <div class="posts-grid"></div>
          <div class="text-center mt-6">
            <a href="articles.html" class="btn btn-primary">TÌM HIỂU THÊM</a>
          </div>
        </div>
      `;

      const grid = container.querySelector(".posts-grid");

      if (limit) data = data.slice(0, limit);

      data.forEach(post => {
        const card = document.createElement("div");
        card.className = "post-card";
        card.innerHTML = `
          <div class="post-thumb">
            <a href="${post.link}">
              <img src="${post.image || 'images/default.jpg'}" alt="${post.title}">
            </a>
          </div>
          <div class="post-info">
            <p class="post-date">${new Date(post.date).toLocaleDateString("vi-VN")}</p>
            <h3 class="post-title">
              <a href="${post.link}">${post.title}</a>
            </h3>
          </div>
        `;
        grid.appendChild(card);
      });
    })
    .catch(err => console.error("Error loading posts:", err));
}
