# 🖼️ VR Tour Gallery Uploader — Share Your Moments in Virtual Reality

This project adds an interactive **user photo upload feature** to a VR tour platform. It allows users to upload their own images (like photos taken at a location) and have them integrated into a **shared virtual gallery** experience.

It’s not a full tour builder — instead, it enhances an existing VR tour by letting users contribute their **memories, moments, or visuals** into the immersive space.

🔗 **Live Preview:** [View Project](https://vrgallery.netlify.app/)

![Preview Screenshot](assets/img1.png)

---

---

## 🎯 What It Does

- 📤 Users upload photos taken at a real-world location
- 🖼️ Uploaded photos appear inside the VR tour or gallery interface
- 🗂️ Images are stored and previewed using a clean gallery layout
- ⚙️ Built with Flask (Python) backend + HTML/CSS frontend

---

## 🗂 Folder Structure

```
VR-Tour_Gallery/
├── Backend/
│ ├── app.py # Handles uploads and routes
│ ├── database.py # (Optional) Logic to manage uploaded files
│ ├── requirements.txt # Python libraries
│ └── render.yaml # Deployment config for Render.com
│
├── Frontend/
│ ├── index.html # Upload UI
│ └── Gallery.html # VR preview page with uploaded images
│
├── image1.png # Sample uploaded image
├── image2.png # Sample uploaded image
├── image3.png # Sample uploaded image
└── README.md # This file
```


---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/thiyo-de/VR-Tour_Gallery.git
cd VR-Tour_Gallery
