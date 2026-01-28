#!/usr/bin/env python3
"""
CTD DOCUMENT ORGANIZER - USING EXISTING STRUCTURE
Uses existing CTD folder structure from organized_ctd
"""

import os
import re
import json
import shutil
import PyPDF2
import pdfplumber
from datetime import datetime
import logging
from typing import Dict, List, Optional, Tuple

# Configuration - EDIT THESE PATHS AS NEEDED
SOURCE_FOLDER = "documents_to_organize"  # Your main folder with m1, m2, etc.
CTD_FOLDER = "organized_ctd"  # Your existing CTD structure
LOG_FILE = "document_organization.log"
MAPPING_FILE = "document_mapping.json"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CTDOrganizer:
    def __init__(self):
        self.folder_mapping = self._build_folder_mapping()
        self.keywords = self._load_keywords()
        self.processed_files = []
        
    def _build_folder_mapping(self) -> Dict[str, str]:
        """Build mapping of CTD sections to folder paths"""
        mapping = {}
        
        if not os.path.exists(CTD_FOLDER):
            print(f"\n❌ CTD folder not found: {CTD_FOLDER}")
            print("Please run the CTD structure builder first.")
            exit(1)
        
        # Walk through the existing CTD structure
        for root, dirs, files in os.walk(CTD_FOLDER):
            # Skip the root folder itself
            if root == CTD_FOLDER:
                continue
            
            # Get the relative path from CTD_FOLDER
            rel_path = os.path.relpath(root, CTD_FOLDER)
            
            # Extract CTD section numbers from folder names
            folder_name = os.path.basename(root)
            
            # Look for CTD section patterns
            section_patterns = [
                r'(\d+(?:\.\d+)+)',  # Matches 1.0, 1.0.1, 1.2.3.4, etc.
                r'(\d+(?:\.\d+)*\s+[A-Za-z])',  # Matches "1.0 Correspondence"
            ]
            
            for pattern in section_patterns:
                matches = re.findall(pattern, folder_name)
                for match in matches:
                    mapping[match] = root
                    # Also map the full folder name
                    mapping[folder_name] = root
            
            # Map common variations
            if "Cover Letter" in folder_name:
                mapping["1.0.1"] = root
                mapping["Cover Letter"] = root
            elif "Application Form" in folder_name:
                mapping["1.2.1"] = root
                mapping["Application Form"] = root
            elif "SmPC" in folder_name or "Summary of Product Characteristics" in folder_name:
                mapping["1.3.1"] = root
                mapping["SmPC"] = root
            elif "PIL" in folder_name or "Patient Information Leaflet" in folder_name:
                mapping["1.3.2"] = root
                mapping["PIL"] = root
            elif "Stability" in folder_name and "3.2.P" in root:
                mapping["3.2.P.8"] = root
                mapping["Stability"] = root
            elif "Toxicology" in folder_name:
                mapping["4.2.3"] = root
                mapping["Toxicology"] = root
            elif "Clinical Study" in folder_name:
                mapping["5.3"] = root
                mapping["Clinical Study"] = root
            elif "Quality Overall Summary" in folder_name:
                mapping["2.3"] = root
                mapping["QOS"] = root
            elif "GMP" in folder_name:
                mapping["GMP"] = root
        
        return mapping
    
    def _load_keywords(self) -> Dict[str, List[str]]:
        """Load CTD section keywords"""
        return {
            "1.0.1": ["cover letter", "submission letter", "application cover", "introductory letter"],
            "1.2.1": ["application form", "regulatory form", "submission form", "form 1"],
            "1.3.1": ["summary of product characteristics", "smc", "smpc", "prescribing information", "product characteristics"],
            "1.3.2": ["patient information leaflet", "pil", "patient leaflet", "medication guide", "patient information"],
            "1.3.3": ["labeling", "labels", "container label", "packaging label"],
            "1.7": ["gmp", "good manufacturing practice", "manufacturing license", "gmp certificate"],
            "2.3": ["quality overall summary", "qos", "module 2.3", "quality summary"],
            "3.2.P.8": ["stability", "shelf life", "storage condition", "stability study", "accelerated stability"],
            "3.2.S.7": ["drug substance stability", "api stability", "active ingredient stability"],
            "4.2.1": ["pharmacology", "pharmacodynamic", "safety pharmacology"],
            "4.2.2": ["pharmacokinetics", "pk", "adme", "absorption", "distribution", "metabolism", "excretion"],
            "4.2.3": ["toxicology", "toxicity", "safety study", "toxicological", "safety assessment"],
            "5.2": ["clinical overview", "clinical summary"],
            "5.3": ["clinical study", "clinical trial", "study report", "clinical report", "trial report", "csr"],
            "5.3.1": ["biopharmaceutics", "bioavailability", "bioequivalence", "ba", "be", "ivivc"],
            "5.3.3": ["pharmacokinetic", "pk study", "human pk", "healthy subject pk"],
            "5.3.4": ["pharmacodynamic", "pd study", "human pd"],
            "5.3.5": ["efficacy", "safety", "clinical efficacy", "clinical safety", "controlled study", "randomized"],
        }
    
    def find_all_pdfs(self) -> List[str]:
        """Recursively find all PDF files in source folder"""
        pdf_files = []
        
        if not os.path.exists(SOURCE_FOLDER):
            print(f"\n❌ Source folder not found: {SOURCE_FOLDER}")
            os.makedirs(SOURCE_FOLDER, exist_ok=True)
            print(f"Created folder. Please add your documents and run again.")
            return []
        
        print(f"\n🔍 Scanning {SOURCE_FOLDER} for PDF files...")
        
        for root, dirs, files in os.walk(SOURCE_FOLDER):
            for file in files:
                if file.lower().endswith('.pdf'):
                    full_path = os.path.join(root, file)
                    pdf_files.append(full_path)
        
        return pdf_files
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        try:
            text = ""
            # Try pdfplumber first
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages[:5]:  # First 5 pages
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                logger.warning(f"pdfplumber failed: {e}")
                # Fallback to PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages[:3]:  # First 3 pages
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            
            return text
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def analyze_document(self, text: str, filename: str) -> Dict:
        """Analyze document content and filename"""
        text_lower = text.lower()
        filename_lower = filename.lower()
        
        # Track scores for each CTD section
        scores = {}
        
        # 1. Check filename for CTD indicators
        for section, folder_path in self.folder_mapping.items():
            if section.lower() in filename_lower:
                scores[section] = scores.get(section, 0) + 50
        
        # 2. Check content with keywords
        for section, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[section] = scores.get(section, 0) + 10
                if keyword in filename_lower:
                    scores[section] = scores.get(section, 0) + 20
        
        # 3. Look for CTD section numbers in text
        section_patterns = [
            r'\bctd\s*(?:section)?\s*[:]?\s*([0-9]+(?:\.[0-9]+)+)\b',
            r'\bsection\s*([0-9]+(?:\.[0-9]+)+)\b',
            r'\bmodule\s*([0-9]+(?:\.[0-9]+)*)\b',
        ]
        
        for pattern in section_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                scores[match] = scores.get(match, 0) + 100
        
        return scores
    
    def get_destination(self, scores: Dict, filename: str) -> Tuple[str, str]:
        """Get destination folder based on scores"""
        if not scores:
            # No matches found
            uncategorized_path = os.path.join(CTD_FOLDER, "Uncategorized")
            os.makedirs(uncategorized_path, exist_ok=True)
            return uncategorized_path, "Uncategorized (no matches found)"
        
        # Sort by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Try to find the highest scoring section in folder mapping
        for section, score in sorted_scores:
            # First try exact section match
            if section in self.folder_mapping:
                return self.folder_mapping[section], f"CTD Section {section} (score: {score})"
            
            # Try partial matches
            for mapped_section, folder_path in self.folder_mapping.items():
                if section in mapped_section or mapped_section in section:
                    return folder_path, f"CTD Section {mapped_section} (score: {score})"
        
        # Try common patterns in filename
        if "cover" in filename.lower():
            for section, folder_path in self.folder_mapping.items():
                if "cover" in section.lower() or "1.0.1" in section:
                    return folder_path, "Filename suggests Cover Letter"
        
        if "application" in filename.lower() or "form" in filename.lower():
            for section, folder_path in self.folder_mapping.items():
                if "application" in section.lower() or "1.2.1" in section:
                    return folder_path, "Filename suggests Application Form"
        
        if "stability" in filename.lower():
            for section, folder_path in self.folder_mapping.items():
                if "stability" in section.lower() or "3.2.P.8" in section:
                    return folder_path, "Filename suggests Stability"
        
        if "clinical" in filename.lower() or "study" in filename.lower():
            for section, folder_path in self.folder_mapping.items():
                if "clinical" in section.lower() or "5.3" in section:
                    return folder_path, "Filename suggests Clinical Study"
        
        if "toxicology" in filename.lower() or "tox" in filename.lower():
            for section, folder_path in self.folder_mapping.items():
                if "toxicology" in section.lower() or "4.2.3" in section:
                    return folder_path, "Filename suggests Toxicology"
        
        if "gmp" in filename.lower():
            for section, folder_path in self.folder_mapping.items():
                if "gmp" in section.lower():
                    return folder_path, "Filename suggests GMP"
        
        # Default to Uncategorized
        uncategorized_path = os.path.join(CTD_FOLDER, "Uncategorized")
        os.makedirs(uncategorized_path, exist_ok=True)
        return uncategorized_path, f"No confident match found (top score: {sorted_scores[0][0]}={sorted_scores[0][1]})"
    
    def organize_file(self, source_path: str, dest_folder: str) -> str:
        """Copy file to destination with unique name"""
        filename = os.path.basename(source_path)
        name_part, ext_part = os.path.splitext(filename)
        
        # Get module information from source path
        module_name = ""
        rel_path = os.path.relpath(source_path, SOURCE_FOLDER)
        path_parts = rel_path.split(os.sep)
        if path_parts and re.match(r'^m\d+$', path_parts[0], re.I):
            module_name = path_parts[0]
        
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if module_name:
            new_filename = f"{module_name}_{name_part}_{timestamp}{ext_part}"
        else:
            new_filename = f"{name_part}_{timestamp}{ext_part}"
        
        dest_path = os.path.join(dest_folder, new_filename)
        
        # Handle duplicates
        counter = 1
        while os.path.exists(dest_path):
            new_filename = f"{name_part}_{timestamp}_{counter}{ext_part}"
            dest_path = os.path.join(dest_folder, new_filename)
            counter += 1
        
        # Copy file
        os.makedirs(dest_folder, exist_ok=True)
        shutil.copy2(source_path, dest_path)
        
        return dest_path
    
    def process_documents(self):
        """Main processing function"""
        print("=" * 60)
        print("CTD DOCUMENT ORGANIZER")
        print("=" * 60)
        
        # Check if CTD structure exists
        if not os.path.exists(CTD_FOLDER):
            print(f"\n❌ CTD folder not found: {CTD_FOLDER}")
            print("Please run the CTD structure builder first.")
            return
        
        print(f"\n📁 Using existing CTD structure: {CTD_FOLDER}")
        print(f"🔍 Found {len(self.folder_mapping)} CTD sections mapped")
        
        # Find all PDFs
        pdf_files = self.find_all_pdfs()
        
        if not pdf_files:
            print(f"\n❌ No PDF files found in {SOURCE_FOLDER}")
            print(f"\nExpected structure:")
            print(f"  {SOURCE_FOLDER}/")
            print(f"  ├── m1/")
            print(f"  │   ├── subfolder1/")
            print(f"  │   │   └── document.pdf")
            print(f"  │   └── ...")
            print(f"  ├── m2/")
            print(f"  └── ...")
            return
        
        print(f"✅ Found {len(pdf_files)} PDF file(s)")
        
        # Show modules found
        modules = set()
        for pdf in pdf_files:
            rel_path = os.path.relpath(pdf, SOURCE_FOLDER)
            parts = rel_path.split(os.sep)
            if parts and re.match(r'^m\d+$', parts[0], re.I):
                modules.add(parts[0])
        
        if modules:
            print(f"📦 Modules found: {', '.join(sorted(modules))}")
        
        print(f"\n{'─' * 40}")
        print("Starting organization...")
        print(f"{'─' * 40}")
        
        # Process each file
        organized_count = 0
        failed_count = 0
        
        for i, pdf_file in enumerate(pdf_files, 1):
            try:
                filename = os.path.basename(pdf_file)
                rel_path = os.path.relpath(pdf_file, SOURCE_FOLDER)
                
                print(f"\n[{i}/{len(pdf_files)}] Processing: {filename}")
                print(f"   📍 Source: {rel_path}")
                
                # Extract text
                text = self.extract_text(pdf_file)
                
                if not text.strip():
                    print("   ⚠️  Could not extract text, using filename only")
                    text = filename
                
                # Analyze document
                scores = self.analyze_document(text, filename)
                
                # Get destination
                dest_folder, reason = self.get_destination(scores, filename)
                
                # Organize file
                dest_path = self.organize_file(pdf_file, dest_folder)
                
                # Get relative path for display
                dest_rel = os.path.relpath(dest_path, CTD_FOLDER)
                dest_parts = dest_rel.split(os.sep)
                display_path = " → ".join(dest_parts)
                
                print(f"   📋 Classification: {reason}")
                print(f"   📂 Destination: {display_path}")
                
                # Record processing
                self.processed_files.append({
                    "source": pdf_file,
                    "destination": dest_path,
                    "classification": reason,
                    "filename": filename,
                    "source_path": rel_path,
                    "timestamp": datetime.now().isoformat()
                })
                
                organized_count += 1
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                failed_count += 1
                logger.error(f"Error processing {pdf_file}: {e}")
        
        # Save mapping
        self._save_mapping()
        
        # Print summary
        self._print_summary(organized_count, failed_count, pdf_files)
    
    def _save_mapping(self):
        """Save mapping to JSON file"""
        if self.processed_files:
            mapping_data = {
                "timestamp": datetime.now().isoformat(),
                "source_folder": SOURCE_FOLDER,
                "ctd_folder": CTD_FOLDER,
                "total_files": len(self.processed_files),
                "mappings": self.processed_files,
                "folder_mapping_summary": {k: os.path.relpath(v, CTD_FOLDER) 
                                          for k, v in list(self.folder_mapping.items())[:20]}  # First 20
            }
            
            with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
                json.dump(mapping_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n📝 Mapping saved to: {MAPPING_FILE}")
    
    def _print_summary(self, organized: int, failed: int, pdf_files: List[str]):
        """Print summary of processing"""
        print(f"\n{'=' * 60}")
        print("ORGANIZATION COMPLETE!")
        print(f"{'=' * 60}")
        
        print(f"\n📊 RESULTS:")
        print(f"   Total PDFs found: {len(pdf_files)}")
        print(f"   Successfully organized: {organized}")
        print(f"   Failed: {failed}")
        
        # Show distribution
        if self.processed_files:
            distribution = {}
            for item in self.processed_files:
                dest_folder = os.path.dirname(item['destination'])
                folder_name = os.path.basename(dest_folder)
                distribution[folder_name] = distribution.get(folder_name, 0) + 1
            
            print(f"\n📁 DISTRIBUTION:")
            sorted_dist = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
            for folder, count in sorted_dist[:10]:  # Top 10
                print(f"   • {folder}: {count} file(s)")
            
            if len(sorted_dist) > 10:
                print(f"   • ... and {len(sorted_dist) - 10} more folders")
        
        print(f"\n📂 Organized files are in: {CTD_FOLDER}")
        print(f"📝 Log file: {LOG_FILE}")
        print(f"📋 Mapping file: {MAPPING_FILE}")
        
        # Show example of where files went
        print(f"\n📌 EXAMPLE DESTINATIONS:")
        for item in self.processed_files[:3]:  # First 3
            filename = item['filename']
            dest_rel = os.path.relpath(item['destination'], CTD_FOLDER)
            print(f"   • {filename[:30]}... → {dest_rel}")

def main():
    """Main function"""
    print("\n" + "="*60)
    print("CTD DOCUMENT ORGANIZER - USING EXISTING STRUCTURE")
    print("="*60)
    
    print(f"\nThis will:")
    print(f"1. Scan {SOURCE_FOLDER} for PDFs in modules (m1, m2, etc.)")
    print(f"2. Use existing CTD structure in {CTD_FOLDER}")
    print(f"3. Classify and organize documents")
    print(f"4. Preserve source module information")
    
    response = input("\nStart organizing documents? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Operation cancelled.")
        return
    
    # Create organizer and process
    organizer = CTDOrganizer()
    organizer.process_documents()

if __name__ == "__main__":
    try:
        import PyPDF2
        import pdfplumber
    except ImportError:
        print("ERROR: Required packages not installed.")
        print("\nPlease install with:")
        print("pip install PyPDF2 pdfplumber")
        exit(1)
    
    main()