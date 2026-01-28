#!/usr/bin/env python3
"""
CTD DOCUMENT ORGANIZER
Extracts information from PDFs and organizes them into CTD structure
"""

import os
import re
import json
import shutil
import hashlib
import PyPDF2
import pdfplumber
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
import logging

# Configuration
CTD_STRUCTURE_FILE = "ctd_structure.json"
CTD_FOLDER = "organized_ctd"
SOURCE_FOLDER = "documents_to_organize"
LOG_FILE = "document_organization.log"

# Set up logging with Unicode handling for Windows
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Enhanced Keywords mapping for CTD sections with precise folder targeting
CTD_KEYWORDS = {
    # Module 1 - Correspondence
    "1.0.1 Cover Letter": ["cover letter", "application cover letter", "submission cover letter", 
                          "official cover letter", "regulatory cover letter", "letter of application"],
    "1.0.2 General Note to Reviewer": ["note to reviewer", "reviewer note", "general note", 
                                      "explanatory note", "review note"],
    "1.0.3 Life Cycle Management Tracking Table": ["life cycle management", "lifecycle", "product lifecycle",
                                                  "management tracking", "tracking table"],
    "1.0.4 Correspondence Issued by Regulatory Authority": ["regulatory authority correspondence", 
                                                          "authority correspondence", "regulatory letter received", 
                                                          "agency correspondence"],
    "1.0.5 Response to Information Solicited by Regulatory Authority": ["response to query", "query response", 
                                                                      "information response", "response to regulatory", 
                                                                      "questions and answers"],
    "1.0.6 Meeting Information": ["meeting minutes", "meeting notes", "meeting summary", "pre-meeting information", 
                                 "post-meeting follow-up"],
    "1.0.7 Request for Appeal Documentation": ["appeal documentation", "request for appeal", "appeal letter",
                                              "regulatory appeal", "appeal request"],
    
    # Module 1 - Administrative Information
    "1.2.1 Application Form": ["application form", "submission application", "regulatory application",
                              "marketing application", "application dossier"],
    "1.2.2 Fee Forms": ["fee form", "payment form", "fee payment", "administrative fee", "regulatory fee", 
                       "processing fee"],
    "1.2.3 Certification and Attestation Forms": ["certification form", "attestation form", "declaration form",
                                                 "certificate", "attestation", "declaration"],
    "1.2.4 Compliance and Site Information": ["site information", "compliance information", "manufacturing site",
                                             "facility information"],
    "1.2.5 Authorization for Sharing Information": ["authorization form", "sharing authorization", "information sharing",
                                                   "data sharing authorization"],
    "1.2.6 Electronic Declaration": ["electronic declaration", "e-declaration", "digital declaration"],
    "1.2.7 Trademark & Intellectual Property Information": ["trademark", "intellectual property", "ip", "brand name",
                                                          "trade name", "proprietary name"],
    "1.2.8 Screening Details": ["screening", "pre-screening", "regulatory screening"],
    
    # Module 1 - Product Information
    "1.3.1 Summary of Product Characteristics": ["summary of product characteristics", "smc", "product characteristics",
                                                "prescribing information"],
    "1.3.2 Patient Information Leaflet": ["patient information leaflet", "pil", "patient leaflet", "patient information",
                                         "medication guide"],
    "1.3.3 Container Labels": ["container label", "primary label", "secondary label", "package label", "outer label",
                              "inner label"],
    "1.3.4 Foreign Labelling": ["foreign labelling", "foreign labeling", "export labelling", "international labelling",
                               "multicountry labelling"],
    "1.3.5 Reference Product Labelling": ["reference product", "comparator labelling", "reference labelling",
                                         "originator labelling"],
    "1.3.6 Artwork and Samples": ["artwork", "sample artwork", "label artwork", "mock-up", "sample", "prototype"],
    
    # Module 1 - GMP
    "1.7.1 Date of Inspection of Each Site": ["inspection date", "site inspection date", "gmp inspection date"],
    "1.7.2 Inspection Reports or Equivalent Documents": ["inspection report", "gmp inspection", "regulatory inspection",
                                                        "site inspection", "facility inspection"],
    "1.7.3 GMP Certificates or Manufacturing Licences": ["gmp certificate", "manufacturing license", "manufacturing authorization",
                                                         "gmp compliance certificate", "site license"],
    "1.7.4 Other GMP Documents": ["gmp documentation", "gmp compliance", "gmp related"],
    
    # Module 2 - Summaries
    "2.3 Quality Overall Summary": ["quality overall summary", "qos", "module 2.3", "drug substance summary", 
                                   "drug product summary"],
    "2.4 Nonclinical Overview": ["nonclinical overview", "preclinical overview", "module 2.4"],
    "2.5 Clinical Overview": ["clinical overview", "module 2.5", "medical overview"],
    
    # Module 3 - Quality
    "3.2.S Drug Substance": ["drug substance", "active substance", "api", "active pharmaceutical ingredient"],
    "3.2.P Drug Product": ["drug product", "finished product", "formulation", "composition"],
    "3.2.P.8 Stability": ["stability", "stability study", "shelf life", "storage condition"],
    
    # Module 4 - Nonclinical
    "4.2.1 Pharmacology": ["pharmacology", "pharmacodynamic", "primary pharmacodynamics", "secondary pharmacodynamics",
                          "safety pharmacology"],
    "4.2.2 Pharmacokinetics": ["pharmacokinetics", "pk", "adme", "absorption", "distribution", "metabolism", "excretion"],
    "4.2.3 Toxicology": ["toxicology", "toxicity study", "single dose toxicity", "repeat dose toxicity", "genotoxicity",
                        "carcinogenicity", "reproductive toxicity", "developmental toxicity"],
    
    # Module 5 - Clinical
    "5.3 Clinical Study Reports": ["clinical study", "clinical trial", "study report", "clinical report", "study protocol"],
    "5.3.1 Reports of Biopharmaceutic Studies": ["biopharmaceutics", "bioavailability", "bioequivalence", "ba", "be"],
    "5.3.5 Reports of Efficacy and Safety Studies": ["efficacy", "effectiveness", "clinical efficacy", "safety"],
}


class PDFProcessor:
    """Process PDF files to extract information"""
    
    def __init__(self):
        self.text_cache = {}
        self.folder_index = {}
    
    def build_folder_index(self, ctd_structure: Dict, base_path: str = ""):
        """Build an index of all CTD folders for quick lookup"""
        folder_index = {}
        
        def index_node(node: Dict, current_path: str):
            node_name = node.get("name", "")
            if node_name:
                folder_name = self._clean_folder_name(node_name)
                full_path = os.path.join(current_path, folder_name) if current_path else folder_name
                
                # Index by full path
                folder_index[full_path] = {
                    "name": node_name,
                    "path": full_path,
                    "description": node.get("description", ""),
                    "is_leaf": not node.get("children")
                }
                
                # Also index by section numbers if present
                section_match = re.search(r'(\d+(?:\.\d+)*)', node_name)
                if section_match:
                    section = section_match.group(1)
                    folder_index[section] = {
                        "name": node_name,
                        "path": full_path,
                        "description": node.get("description", ""),
                        "is_leaf": not node.get("children")
                    }
                
                # Index children
                children = node.get("children", [])
                for child in children:
                    index_node(child, full_path)
        
        index_node(ctd_structure, base_path)
        self.folder_index = folder_index
        return folder_index
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            # Check cache first
            pdf_hash = self._get_file_hash(pdf_path)
            if pdf_hash in self.text_cache:
                return self.text_cache[pdf_hash]
            
            text = ""
            
            # Try pdfplumber first (better for complex layouts)
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                logger.warning(f"pdfplumber failed for {pdf_path}: {e}")
                # Fallback to PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            
            # Cache the result
            self.text_cache[pdf_hash] = text
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def analyze_content(self, text: str, filename: str = "") -> Dict:
        """Analyze PDF content to determine CTD section"""
        text_lower = text.lower()
        filename_lower = filename.lower() if filename else ""
        
        # Initialize scores for each CTD folder
        scores = {folder: 0 for folder in CTD_KEYWORDS}
        
        # Score based on keywords in text
        for folder_name, keywords in CTD_KEYWORDS.items():
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                # Check in text
                if keyword_lower in text_lower:
                    # Count occurrences with weight
                    count = text_lower.count(keyword_lower)
                    scores[folder_name] += count * 5
                
                # Check in filename
                if filename and keyword_lower in filename_lower:
                    scores[folder_name] += 50
        
        # Look for CTD section numbers in text
        found_sections = self._extract_ctd_sections(text_lower)
        
        return {
            "scores": scores,
            "found_sections": found_sections,
            "text_sample": text[:500] if len(text) > 500 else text,
        }
    
    def _extract_ctd_sections(self, text: str) -> List[str]:
        """Extract CTD section numbers from text"""
        patterns = [
            r'\b(?:ctd|module)\s*(?:section)?\s*[:]?\s*([0-9]+(?:\.[0-9]+)+)\b',
            r'\bsection\s*([0-9]+(?:\.[0-9]+)+)\b',
            r'\b([0-9]+\.[0-9]+(?:\.[0-9]+)*)\b'
        ]
        
        sections = set()
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                section = match.strip()
                if section.count('.') >= 1:
                    sections.add(section)
        
        return list(sections)
    
    def _clean_folder_name(self, name: str) -> str:
        """Clean folder name"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '-')
        return ' '.join(name.split())
    
    def _get_file_hash(self, file_path: str) -> str:
        """Generate hash for file"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()


class CTDOrganizer:
    """Organize documents into CTD structure with precise folder matching"""
    
    def __init__(self, ctd_structure_file: str = CTD_STRUCTURE_FILE):
        self.ctd_structure = self._load_ctd_structure(ctd_structure_file)
        self.pdf_processor = PDFProcessor()
        self.pdf_processor.build_folder_index(self.ctd_structure, CTD_FOLDER)
        self.mapping_log = []
        self.all_folders = self._get_all_folder_paths()
        
    def _load_ctd_structure(self, structure_file: str) -> Dict:
        """Load CTD structure from JSON file"""
        try:
            with open(structure_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"CTD structure file not found: {structure_file}")
            raise
    
    def _get_all_folder_paths(self) -> Dict[str, str]:
        """Get all folder paths in the CTD structure"""
        folder_paths = {}
        
        def traverse_node(node: Dict, current_path: str):
            node_name = node.get("name", "")
            if node_name:
                folder_name = self._clean_folder_name(node_name)
                full_path = os.path.join(current_path, folder_name) if current_path else folder_name
                folder_paths[node_name] = full_path
                
                # Also add section number if present
                section_match = re.search(r'(\d+(?:\.\d+)*)', node_name)
                if section_match:
                    folder_paths[section_match.group(1)] = full_path
                
                children = node.get("children", [])
                for child in children:
                    traverse_node(child, full_path)
        
        traverse_node(self.ctd_structure, CTD_FOLDER)
        return folder_paths
    
    def find_exact_ctd_folder(self, analysis_result: Dict, filename: str = "") -> Tuple[str, str]:
        """Find the exact CTD folder for the document"""
        scores = analysis_result["scores"]
        found_sections = analysis_result.get("found_sections", [])
        
        # Strategy 1: Direct section number match
        for section in found_sections:
            # Try exact match first
            if section in self.all_folders:
                folder_path = self.all_folders[section]
                if os.path.exists(folder_path):
                    return folder_path, f"Exact CTD section match: {section}"
            
            # Try partial match
            for known_section in self.all_folders.keys():
                if isinstance(known_section, str) and known_section.startswith(section):
                    folder_path = self.all_folders[known_section]
                    if os.path.exists(folder_path):
                        return folder_path, f"Partial CTD section match: {section} -> {known_section}"
        
        # Strategy 2: Keyword score match
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        if sorted_scores:
            top_folder, top_score = sorted_scores[0]
            if top_score > 10:
                # Find this folder in our structure
                for folder_name, folder_path in self.all_folders.items():
                    if top_folder in folder_name:
                        if os.path.exists(folder_path):
                            return folder_path, f"Keyword match: {top_folder}"
        
        # Strategy 3: Filename-based matching
        if filename:
            folder_from_filename = self._match_from_filename(filename)
            if folder_from_filename:
                return folder_from_filename, f"Filename match: {filename}"
        
        # Default to Uncategorized
        uncategorized_path = os.path.join(CTD_FOLDER, "Uncategorized")
        os.makedirs(uncategorized_path, exist_ok=True)
        return uncategorized_path, "No match found"
    
    def _match_from_filename(self, filename: str) -> Optional[str]:
        """Match folder based on filename patterns"""
        filename_lower = filename.lower()
        
        # Common patterns in filenames
        patterns = [
            (["cover letter", "cover-letter", "cover_letter", "emea-cover", "ema-cover"], "1.0.1 Cover Letter"),
            (["application form", "application-form", "appform", "emea-form", "ema-form"], "1.2.1 Application Form"),
            (["gmp certificate", "gmp-cert"], "1.7.3 GMP Certificates or Manufacturing Licences"),
            (["smc", "summary of product"], "1.3.1 Summary of Product Characteristics (SmPC)"),
            (["pil", "patient leaflet"], "1.3.2 Patient Information Leaflet (PIL)"),
            (["clinical study", "study-report", "clinical-trial"], "5.3 Clinical Study Reports and Related Information"),
            (["protocol", "study-protocol"], "5.3 Clinical Study Reports and Related Information"),
            (["quality summary", "qos"], "2.3 Quality Overall Summary (QOS)"),
            (["stability", "stability-study"], "3.2.P.8 Stability"),
            (["specification", "spec"], "3.2.P.5 Control of Drug Product"),
        ]
        
        for pattern_list, folder_name in patterns:
            for pattern in pattern_list:
                if pattern in filename_lower:
                    # Find the exact folder path
                    for known_name, folder_path in self.all_folders.items():
                        if folder_name in known_name:
                            return folder_path
        
        return None
    
    def _clean_folder_name(self, name: str) -> str:
        """Clean folder name"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '-')
        return ' '.join(name.split())
    
    def organize_document(self, source_path: str, dest_folder: str) -> str:
        """Organize a single document WITHOUT creating JSON metadata"""
        filename = os.path.basename(source_path)
        name_part, ext_part = os.path.splitext(filename)
        
        # Create clean destination filename
        dest_filename = f"{name_part}{ext_part}"
        dest_path = os.path.join(dest_folder, dest_filename)
        
        # Handle duplicates
        counter = 1
        while os.path.exists(dest_path):
            dest_filename = f"{name_part}_{counter}{ext_part}"
            dest_path = os.path.join(dest_folder, dest_filename)
            counter += 1
        
        # Ensure destination folder exists
        os.makedirs(dest_folder, exist_ok=True)
        
        # Copy file (preserve metadata) - NO JSON METADATA CREATED
        shutil.copy2(source_path, dest_path)
        
        return dest_path
    
    def process_folder(self, source_folder: str = SOURCE_FOLDER):
        """Process all documents in source folder"""
        if not os.path.exists(source_folder):
            logger.error(f"Source folder not found: {source_folder}")
            return
        
        # Get all PDF files
        pdf_files = []
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {source_folder}")
            return
        
        print(f"\n{'='*60}")
        print("ORGANIZING DOCUMENTS...")
        print('='*60)
        
        print(f"\nFound {len(pdf_files)} PDF files to process")
        
        processed_count = 0
        for pdf_file in pdf_files:
            try:
                filename = os.path.basename(pdf_file)
                print(f"\n[PROCESSING] {filename}")
                
                # Extract text and analyze
                text = self.pdf_processor.extract_text_from_pdf(pdf_file)
                if not text.strip():
                    print(f"  [!] No text extracted, skipping")
                    continue
                
                analysis = self.pdf_processor.analyze_content(text, filename)
                
                # Find exact CTD folder
                dest_folder, reason = self.find_exact_ctd_folder(analysis, filename)
                
                # Organize document (NO JSON metadata created)
                dest_path = self.organize_document(pdf_file, dest_folder)
                
                # Get relative path for display
                rel_path = os.path.relpath(dest_path, CTD_FOLDER)
                
                # Show clear path where file went
                print(f"  ┌─[ORGANIZED TO]")
                
                # Split and display path
                path_parts = rel_path.split(os.sep)
                display_path = ""
                for i, part in enumerate(path_parts):
                    if i == 0:
                        display_path = f"📁 {part}"
                    else:
                        display_path += f" → 📁 {part}"
                
                print(f"  │ {display_path}")
                print(f"  └─[REASON] {reason}")
                
                self.mapping_log.append({
                    "source": pdf_file,
                    "destination": dest_path,
                    "reason": reason,
                    "filename": filename,
                })
                
                processed_count += 1
                
            except Exception as e:
                print(f"  [!] Error: {e}")
                logger.error(f"Error processing {pdf_file}: {e}")
        
        # Save mapping log (optional - only for reference)
        self._save_mapping_log()
        
        print(f"\n{'='*60}")
        print("ORGANIZATION COMPLETE!")
        print('='*60)
        
        # Show only total count, not folder-by-folder summary
        print(f"\n✅ Successfully organized {processed_count} out of {len(pdf_files)} files")
        print(f"📁 All files are now in: {CTD_FOLDER}")
        
        # REMOVED: The folder-by-folder count summary
    
    def _save_mapping_log(self):
        """Save mapping log to JSON file (optional, for reference only)"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "total_documents": len(self.mapping_log),
            "mappings": self.mapping_log
        }
        
        with open("organized_mapping.json", 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)


def main():
    """Main function"""
    print("=" * 60)
    print("CTD DOCUMENT ORGANIZER")
    print("=" * 60)
    
    # Check if CTD structure exists
    if not os.path.exists(CTD_FOLDER):
        print(f"ERROR: CTD structure not found: {CTD_FOLDER}")
        print("Please run the structure builder first:")
        print("python create_ctd_structure.py")
        return
    
    # Check if source folder exists
    if not os.path.exists(SOURCE_FOLDER):
        print(f"WARNING: Source folder not found: {SOURCE_FOLDER}")
        print("Creating source folder...")
        os.makedirs(SOURCE_FOLDER, exist_ok=True)
        print(f"CREATED: {SOURCE_FOLDER}")
        print(f"\nPlease add your PDF documents to: {SOURCE_FOLDER}")
        print("Then run this script again.")
        return
    
    # Check for PDFs
    pdf_count = sum(1 for root, dirs, files in os.walk(SOURCE_FOLDER) 
                   for file in files if file.lower().endswith('.pdf'))
    
    if pdf_count == 0:
        print(f"WARNING: No PDF files found in: {SOURCE_FOLDER}")
        print(f"\nPlease add PDF documents to: {SOURCE_FOLDER}")
        return
    
    print(f"\nReady to organize {pdf_count} PDF files")
    print("CTD structure loaded from: organized_ctd")
    
    # Start organization
    response = input("\nStart organizing documents? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Operation cancelled.")
        return
    
    # Initialize organizer and process
    organizer = CTDOrganizer()
    organizer.process_folder()


if __name__ == "__main__":
    # Check for required packages
    try:
        import PyPDF2
        import pdfplumber
    except ImportError:
        print("ERROR: Required packages not installed.")
        print("\nPlease install required packages:")
        print("pip install PyPDF2 pdfplumber")
        exit(1)
    
    main()