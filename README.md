## AI Recipe Generator

Welcome to the AI Recipe Generator! This project leverages advanced machine learning techniques to recommend recipes based on the ingredients you have at hand. Say goodbye to meal planning struggles and hello to delightful cooking experiences with just a few clicks.

### Features

- **Ingredient-Based Recommendations**: Enter your available ingredients and receive personalized recipe suggestions.
- **Comprehensive Details**: Each recipe includes preparation time, cooking time, ingredients list, and step-by-step instructions.
- **Visual Experience**: Explore recipes with accompanying images for a delightful culinary journey.
- **User-Friendly Interface**: The intuitive web interface, powered by Streamlit, ensures a seamless user experience.

### Technologies Used

- **Machine Learning**: TensorFlow and pandas handle data processing and modeling.
- **Frontend Development**: Built using Streamlit for a responsive and engaging UI.
- **Data Handling**: Efficient preprocessing ensures accurate recommendations.

### Getting Started

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/Nivetha2005/AI-Recipe-Generator.git
    cd AI-Recipe-Generator
    ```

2. **Install Dependencies**:
    - Ensure Python 3.x and Anaconda are installed.
    - Create a virtual environment and install required packages:
      ```sh
      conda create -n recipe-gen python=3.x
      conda activate recipe-gen
      pip install -r requirements.txt
      ```

3. **Run the Application**:
    - Start the Streamlit server to run the AI Recipe Generator app:
      ```sh
      streamlit run app.py
      ```

4. **Explore Recipes**:
    - Open your browser and navigate to the provided localhost URL to access the AI Recipe Generator.
    - Enter your ingredients and enjoy personalized recipe suggestions.

### Project Structure

- **app.py**: Main code for the AI Recipe Generator.
- **data/**: Data files and datasets.
- **models/**: Trained ML models and preprocessing scripts.
- **static/**: Assets like images and CSS files.

### Contributing

Contributions to enhance the AI Recipe Generator are welcome! Please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Acknowledgements

Special thanks to the open-source community for their valuable contributions and resources.
