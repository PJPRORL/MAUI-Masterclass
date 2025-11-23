# 📱 .NET MAUI Learning Platform & Playground

![.NET MAUI](https://img.shields.io/badge/.NET%20MAUI-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)
![Blazor](https://img.shields.io/badge/Blazor-5C2D91?style=for-the-badge&logo=blazor&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

Welcome to the **MAUI Learning Platform**, an interactive web application designed to teach **.NET MAUI** concepts (MVVM, Dependency Injection, Data Binding) directly in the browser. 

This project features a unique **"Mini-IDE" Playground** that allows users to write, edit, and run simulated MAUI code without installing Visual Studio!

---

## ✨ Key Features

### 🛠️ Interactive MAUI Playground (Mini-IDE)
The crown jewel of this platform. It simulates a real .NET MAUI environment entirely in the browser using Blazor WebAssembly.
- **File Explorer**: Create, delete, and manage multiple files (`Views`, `ViewModels`, `Services`).
- **Live Preview**: See your XAML and C# changes instantly rendered.
- **MVVM Simulation**: Full support for `INotifyPropertyChanged`, `RelayCommand`, and Data Binding.
- **Dependency Injection**: Simulate service registration and injection into ViewModels.
- **Monaco Editor**: Professional code editing experience (VS Code engine) with syntax highlighting.

### 📚 Interactive Chapters
Structured learning modules covering essential MAUI topics:
1.  **MVVM & Data Binding**: Learn the core patterns.
2.  **Repositories & DI**: Structure your data layer.
3.  **Interaction**: Commands and Event Handling.
4.  **Complex Data**: CollectionViews and ObservableCollections.

### 📖 Component Catalog
A built-in reference guide listing properties and attributes for common MAUI controls (`StackLayout`, `Grid`, `Button`, `Entry`, `CollectionView`, etc.), helping beginners discover what's possible.

---

## 🚀 Getting Started

### Prerequisites
- [.NET 8.0 SDK](https://dotnet.microsoft.com/download)

### Installation
1.  Clone the repository:
    ```bash
    git clone https://github.com/YOUR_USERNAME/maui-learning-platform.git
    ```
2.  Navigate to the project folder:
    ```bash
    cd maui-learning-platform/MauiLearningPlatform
    ```
3.  Run the application:
    ```bash
    dotnet run
    ```
4.  Open your browser to `http://localhost:5032`.

---

## 🏗️ Architecture

This project is built as a **Blazor WebAssembly** Standalone app.

- **Frontend**: Blazor WASM + HTML/CSS.
- **Code Editor**: Monaco Editor (via JS Interop).
- **Simulation Engine**: A custom C# parser and runtime that mimics the MAUI XAML engine and Dependency Injection container, allowing "compilation" and execution of user code directly in the browser memory.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new chapters or features for the simulation engine, feel free to open an issue or submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

*Built with ❤️ for the .NET Community.*
