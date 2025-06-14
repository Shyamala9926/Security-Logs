# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import re
import json
from typing import List, Dict
from collections import Counter
import uvicorn

app = FastAPI(title="Log Template Mining API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LogEntry(BaseModel):
    raw_log: str
    timestamp: str = ""

class TemplateResponse(BaseModel):
    templates: List[Dict]
    statistics: Dict

class LogTemplateMiner:
    def __init__(self):
        self.templates = {}
        self.template_patterns = []
        
    def preprocess_log(self, log_line: str) -> str:
        """Basic preprocessing of log lines"""
        # Remove timestamps, IPs, and other variable data
        log_line = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', '<TIMESTAMP>', log_line)
        log_line = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '<IP>', log_line)
        log_line = re.sub(r'\b\d+\b', '<NUM>', log_line)
        log_line = re.sub(r'[a-fA-F0-9]{8,}', '<HASH>', log_line)
        return log_line.strip()
    
    def extract_template_llm_style(self, logs: List[str]) -> Dict:
        """Simple template extraction using pattern matching (simulating LLM approach)"""
        preprocessed_logs = [self.preprocess_log(log) for log in logs]
        
        # Group similar logs
        template_groups = {}
        for i, log in enumerate(preprocessed_logs):
            # Create a simple signature
            words = log.split()
            signature = ' '.join([w for w in words if not w.startswith('<')])
            
            if signature not in template_groups:
                template_groups[signature] = []
            template_groups[signature].append({
                'original': logs[i],
                'processed': log,
                'index': i
            })
        
        # Generate templates
        templates = []
        for signature, group in template_groups.items():
            if len(group) >= 2:  # Only consider patterns that appear multiple times
                template = {
                    'id': len(templates) + 1,
                    'template': group[0]['processed'],
                    'signature': signature,
                    'count': len(group),
                    'examples': [item['original'] for item in group[:3]],
                    'confidence': min(1.0, len(group) / 10)  # Simple confidence score
                }
                templates.append(template)
        
        return {
            'templates': sorted(templates, key=lambda x: x['count'], reverse=True),
            'total_logs': len(logs),
            'unique_templates': len(templates),
            'coverage': sum(t['count'] for t in templates) / len(logs) if logs else 0
        }

miner = LogTemplateMiner()

@app.post("/analyze", response_model=TemplateResponse)
async def analyze_logs(file: UploadFile = File(...)):
    """Analyze uploaded log file and extract templates"""
    try:
        content = await file.read()
        logs = content.decode('utf-8').strip().split('\n')
        logs = [log.strip() for log in logs if log.strip()]
        
        if not logs:
            raise HTTPException(status_code=400, detail="No valid log entries found")
        
        result = miner.extract_template_llm_style(logs)
        
        return TemplateResponse(
            templates=result['templates'],
            statistics={
                'total_logs': result['total_logs'],
                'unique_templates': result['unique_templates'],
                'coverage_percentage': round(result['coverage'] * 100, 2)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing logs: {str(e)}")

@app.post("/analyze-text")
async def analyze_text_logs(logs: List[str]):
    """Analyze logs from text input"""
    try:
        if not logs:
            raise HTTPException(status_code=400, detail="No log entries provided")
        
        result = miner.extract_template_llm_style(logs)
        
        return TemplateResponse(
            templates=result['templates'],
            statistics={
                'total_logs': result['total_logs'],
                'unique_templates': result['unique_templates'],
                'coverage_percentage': round(result['coverage'] * 100, 2)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing logs: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Log Template Mining API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)