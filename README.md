# Security Log Template Mining System

## Project Structure
```
log_template_mining/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   └── index.html
└── sample_logs.txt
```

## Setup Instructions for Windows

### 1. Create Project Directory
```cmd
mkdir log_template_mining
cd log_template_mining
mkdir backend
mkdir frontend
```

### 2. Backend Setup

#### Create backend files:
- **Path**: `backend/main.py` (copy the Python backend code)
- **Path**: `backend/requirements.txt` (copy the requirements)

#### Install Python dependencies:
```cmd
cd backend
pip install -r requirements.txt
```

#### Run the backend server:
```cmd
python main.py
```
The backend will run on `http://localhost:8000`

### 3. Frontend Setup

#### Create frontend file:
- **Path**: `frontend/index.html` (copy the HTML frontend code)

#### Open the frontend:
- Double-click `frontend/index.html` to open in your browser
- Or open VS Code and use Live Server extension

### 4. Sample Data
- **Path**: `sample_logs.txt` (copy the sample log data)

## Usage

1. **Start the backend server**:
   ```cmd
   cd backend
   python main.py
   ```

2. **Open the frontend**:
   - Open `frontend/index.html` in your browser
   - The interface will be available at the file location

3. **Analyze logs**:
   - Upload the `sample_logs.txt` file using the "Choose File" button
   - Or paste log entries directly into the text area
   - Click "Analyze Logs" or "Analyze Text"

## Features

- **Unsupervised Template Mining**: Automatically detects patterns in log files
- **Pattern Recognition**: Identifies recurring log templates
- **Statistical Analysis**: Provides coverage and frequency statistics
- **Web Interface**: User-friendly frontend for log analysis
- **File Upload**: Support for .txt and .log files
- **Real-time Analysis**: Instant results with confidence scores

## API Endpoints

- `POST /analyze` - Analyze uploaded log file
- `POST /analyze-text` - Analyze logs from text input
- `GET /` - Health check

## VS Code Setup

1. Install Python extension
2. Install Live Server extension (optional)
3. Open the project folder in VS Code
4. Use integrated terminal to run backend commands

## Notes

- Ensure Python 3.7+ is installed
- The backend must be running for the frontend to work
- Sample logs are provided for testing
- The system uses simple pattern matching to simulate LLM-based analysis
- Templates are extracted based on log structure and recurring patterns