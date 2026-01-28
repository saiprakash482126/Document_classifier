#!/usr/bin/env python3
"""
CTD STRUCTURE BUILDER
Creates complete CTD folder structure in organized_ctd
"""

import json
import os
import shutil
from typing import Dict, List

# Configuration
CTD_STRUCTURE_FILE = "ctd_structure.json"
OUTPUT_FOLDER = "organized_ctd"

def create_complete_ctd_structure():
    """Create the most comprehensive CTD structure possible"""
    print("=" * 60)
    print("CREATING COMPLETE CTD FOLDER STRUCTURE")
    print("=" * 60)
    
    # Define the most comprehensive CTD structure
    complete_ctd_structure = {
        "name": "CTD Structure",
        "description": "Common Technical Document Structure",
        "children": [
            {
                "name": "Module 1 Administrative Information and Prescribing Information",
                "description": "Administrative documents and product information",
                "children": [
                    {
                        "name": "1.0 Correspondence",
                        "children": [
                            {"name": "1.0.1 Cover Letter", "description": "Cover letters and introductory documents"},
                            {"name": "1.0.2 General Note to Reviewer", "description": "Notes to regulatory reviewers"},
                            {"name": "1.0.3 Life Cycle Management Tracking Table", "description": "Life cycle management documents"},
                            {"name": "1.0.4 Correspondence Issued by Regulatory Authority", "description": "Regulatory authority correspondence"},
                            {"name": "1.0.5 Response to Information Solicited by Regulatory Authority", "description": "Responses to regulatory queries"},
                            {"name": "1.0.6 Meeting Information", "description": "Meeting minutes and notes"},
                            {"name": "1.0.7 Request for Appeal Documentation", "description": "Appeal documentation"}
                        ]
                    },
                    {
                        "name": "1.2 Administrative Information",
                        "children": [
                            {"name": "1.2.1 Application Form", "description": "Regulatory application forms"},
                            {"name": "1.2.2 Fee Forms", "description": "Fee payment forms"},
                            {"name": "1.2.3 Certification and Attestation Forms", "description": "Certification documents"},
                            {"name": "1.2.4 Compliance and Site Information", "description": "Site compliance information"},
                            {"name": "1.2.5 Authorization for Sharing Information", "description": "Information sharing authorizations"},
                            {"name": "1.2.6 Electronic Declaration", "description": "Electronic declarations"},
                            {"name": "1.2.7 Trademark & Intellectual Property Information", "description": "Trademark and IP documents"},
                            {"name": "1.2.8 Screening Details", "description": "Screening information"},
                            {"name": "1.2.A Additional Administrative Information", "description": "Additional administrative documents"}
                        ]
                    },
                    {
                        "name": "1.3 Product Information",
                        "children": [
                            {
                                "name": "1.3.1 Summary of Product Characteristics (SmPC)",
                                "children": [
                                    {
                                        "name": "1.3.1.1 Approved - SmPC",
                                        "children": [
                                            {"name": "1.3.1.1.1 Approved - SmPC - English"},
                                            {"name": "1.3.1.1.2 Approved - SmPC - French"},
                                            {"name": "1.3.1.1.3 Approved - SmPC - Portuguese"}
                                        ]
                                    },
                                    {
                                        "name": "1.3.1.2 Clean - SmPC",
                                        "children": [
                                            {"name": "1.3.1.2.1 Clean - SmPC - English"},
                                            {"name": "1.3.1.2.2 Clean - SmPC - French"},
                                            {"name": "1.3.1.2.3 Clean - SmPC - Portuguese"}
                                        ]
                                    },
                                    {
                                        "name": "1.3.1.3 Annotated - SmPC",
                                        "children": [
                                            {"name": "1.3.1.3.1 Annotated - SmPC - English"},
                                            {"name": "1.3.1.3.2 Annotated - SmPC - French"},
                                            {"name": "1.3.1.3.3 Annotated - SmPC - Portuguese"}
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "1.3.2 Patient Information Leaflet (PIL)",
                                "children": [
                                    {
                                        "name": "1.3.2.1 Approved - PIL",
                                        "children": [
                                            {"name": "1.3.2.1.1 Approved - PIL - English"},
                                            {"name": "1.3.2.1.2 Approved - PIL - French"},
                                            {"name": "1.3.2.1.3 Approved - PIL - Portuguese"}
                                        ]
                                    },
                                    {
                                        "name": "1.3.2.2 Clean - PIL",
                                        "children": [
                                            {"name": "1.3.2.2.1 Clean - PIL - English"},
                                            {"name": "1.3.2.2.2 Clean - PIL - French"},
                                            {"name": "1.3.2.2.3 Clean - PIL - Portuguese"}
                                        ]
                                    },
                                    {
                                        "name": "1.3.2.3 Annotated - PIL",
                                        "children": [
                                            {"name": "1.3.2.3.1 Annotated - PIL - English"},
                                            {"name": "1.3.2.3.2 Annotated - PIL - French"},
                                            {"name": "1.3.2.3.3 Annotated - PIL - Portuguese"}
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "1.3.3 Container Labels",
                                "children": [
                                    {
                                        "name": "1.3.3.1 Approved - Container Labels",
                                        "children": [
                                            {"name": "1.3.3.1.1 Approved - Container Labels - English"},
                                            {"name": "1.3.3.1.2 Approved - Container Labels - French"},
                                            {"name": "1.3.3.1.3 Approved - Container Labels - Portuguese"}
                                        ]
                                    },
                                    {
                                        "name": "1.3.3.2 Clean - Container Labels",
                                        "children": [
                                            {"name": "1.3.3.2.1 Clean - Container Labels - English"},
                                            {"name": "1.3.3.2.2 Clean - Container Labels - French"},
                                            {"name": "1.3.3.2.3 Clean - Container Labels - Portuguese"}
                                        ]
                                    },
                                    {
                                        "name": "1.3.3.3 Annotated - Container Labels",
                                        "children": [
                                            {"name": "1.3.3.3.1 Annotated - Container Labels - English"},
                                            {"name": "1.3.3.3.2 Annotated - Container Labels - French"},
                                            {"name": "1.3.3.3.3 Annotated - Container Labels - Portuguese"}
                                        ]
                                    }
                                ]
                            },
                            {"name": "1.3.4 Foreign Labelling", "description": "Foreign labeling documents"},
                            {"name": "1.3.5 Reference Product Labelling", "description": "Reference product labeling"},
                            {"name": "1.3.6 Artwork and Samples", "description": "Artwork and sample documentation"}
                        ]
                    },
                    {
                        "name": "1.4 Information about the Experts",
                        "children": [
                            {"name": "1.4.1 Quality", "description": "Quality expert information"},
                            {"name": "1.4.2 Non-Clinical", "description": "Non-clinical expert information"},
                            {"name": "1.4.3 Clinical", "description": "Clinical expert information"}
                        ]
                    },
                    {
                        "name": "1.5 Specific Requirements for Different Types of Applications",
                        "children": [
                            {"name": "1.5.1 Bioequivalence Trial Information", "description": "Bioequivalence trial documentation"}
                        ]
                    },
                    {
                        "name": "1.6 Environmental Risk Assessment",
                        "children": [
                            {"name": "1.6.1 Non-GMO", "description": "Non-GMO documentation"},
                            {"name": "1.6.2 GMO", "description": "GMO documentation"}
                        ]
                    },
                    {
                        "name": "1.7 Good Manufacturing Practice (GMP)",
                        "children": [
                            {"name": "1.7.1 Date of Inspection of Each Site", "description": "Site inspection dates"},
                            {"name": "1.7.2 Inspection Reports or Equivalent Documents", "description": "Inspection reports"},
                            {"name": "1.7.3 GMP Certificates or Manufacturing Licences", "description": "GMP certificates"},
                            {"name": "1.7.4 Other GMP Documents", "description": "Other GMP documentation"}
                        ]
                    },
                    {
                        "name": "1.8 Information Relating to Pharmacovigilance",
                        "children": [
                            {"name": "1.8.1 Pharmacovigilance System", "description": "Pharmacovigilance system documentation"},
                            {"name": "1.8.2 Risk-management System", "description": "Risk management documentation"}
                        ]
                    },
                    {"name": "1.9 Individual Patient Data - Statement of Availability", "description": "Patient data availability statements"},
                    {
                        "name": "1.10 Foreign Regulatory Information",
                        "children": [
                            {"name": "1.10.1 Regional & Foreign Regulatory Status", "description": "Regulatory status information"},
                            {"name": "1.10.2 WHO Type Certificate of Pharmaceutical Product (COPP)", "description": "WHO certificates"},
                            {"name": "1.10.3 Data Set Similarities and Differences", "description": "Data set comparisons"},
                            {"name": "1.10.4 Foreign Evaluation Reports", "description": "Foreign evaluation reports"}
                        ]
                    },
                    {
                        "name": "1.A Additional Data",
                        "children": [
                            {"name": "1.A.1 Country Specific Data", "description": "Country-specific documentation"}
                        ]
                    }
                ]
            },
            {
                "name": "Module 2 Common Technical Document Summaries",
                "description": "CTD summaries and overviews",
                "children": [
                    {"name": "2.2 Introduction to Summary", "description": "Summary introduction"},
                    {
                        "name": "2.3 Quality Overall Summary (QOS)",
                        "children": [
                            {"name": "2.3 Introduction", "description": "QOS introduction"},
                            {"name": "2.3.S Drug Substance", "description": "Drug substance summary"},
                            {"name": "2.3.P Drug Product", "description": "Drug product summary"},
                            {"name": "2.3.A Appendices", "description": "QOS appendices"},
                            {"name": "2.3.R Regional Information", "description": "Regional information"}
                        ]
                    },
                    {"name": "2.4 Nonclinical Overview", "description": "Nonclinical overview"},
                    {"name": "2.5 Clinical Overview", "description": "Clinical overview"},
                    {
                        "name": "2.6 NonClinical Written and Tabulated Summaries",
                        "children": [
                            {"name": "2.6.1 Introduction", "description": "Nonclinical summaries introduction"},
                            {"name": "2.6.2 Pharmacology Written Summary", "description": "Pharmacology written summary"},
                            {"name": "2.6.3 Pharmacology Tabulated Summary", "description": "Pharmacology tabulated summary"},
                            {"name": "2.6.4 Pharmacokinetics Written Summary", "description": "PK written summary"},
                            {"name": "2.6.5 Pharmacokinetics Tabulated Summary", "description": "PK tabulated summary"},
                            {"name": "2.6.6 Toxicology Written Summary", "description": "Toxicology written summary"},
                            {"name": "2.6.7 Toxicology Tabulated Summary", "description": "Toxicology tabulated summary"}
                        ]
                    },
                    {
                        "name": "2.7 Clinical Summary",
                        "children": [
                            {"name": "2.7.1 Summary of Biopharmaceutic Studies", "description": "Biopharmaceutics summary"},
                            {"name": "2.7.2 Summary of Clinical Pharmacology Studies", "description": "Clinical pharmacology summary"},
                            {"name": "2.7.3 Summary of Clinical Efficacy", "description": "Clinical efficacy summary"},
                            {"name": "2.7.4 Summary of Clinical Safety", "description": "Clinical safety summary"},
                            {"name": "2.7.5 References", "description": "Clinical references"},
                            {"name": "2.7.6 Synopses of Individual Studies", "description": "Study synopses"}
                        ]
                    }
                ]
            },
            {
                "name": "Module 3 Quality",
                "description": "Quality documentation",
                "children": [
                    {
                        "name": "3.2 Body of Data",
                        "children": [
                            {
                                "name": "3.2.S Drug Substance",
                                "children": [
                                    {
                                        "name": "3.2.S.1 General Information",
                                        "children": [
                                            {"name": "3.2.S.1.1 Nomenclature", "description": "Drug substance nomenclature"},
                                            {"name": "3.2.S.1.2 Structure", "description": "Drug substance structure"},
                                            {"name": "3.2.S.1.3 General Properties", "description": "Drug substance properties"}
                                        ]
                                    },
                                    {"name": "3.2.S.2 Manufacture", "description": "Drug substance manufacture"},
                                    {"name": "3.2.S.3 Characterization", "description": "Drug substance characterization"},
                                    {"name": "3.2.S.4 Control of Drug Substance", "description": "Drug substance control"},
                                    {"name": "3.2.S.5 Reference Standards or Materials", "description": "Reference standards"},
                                    {"name": "3.2.S.6 Container Closure Systems", "description": "Container closure systems"},
                                    {"name": "3.2.S.7 Stability", "description": "Drug substance stability"}
                                ]
                            },
                            {
                                "name": "3.2.P Drug Product",
                                "children": [
                                    {"name": "3.2.P.1 Description and Composition", "description": "Drug product description"},
                                    {"name": "3.2.P.2 Pharmaceutical Development", "description": "Pharmaceutical development"},
                                    {"name": "3.2.P.3 Manufacture", "description": "Drug product manufacture"},
                                    {"name": "3.2.P.4 Control of Excipients", "description": "Excipient control"},
                                    {"name": "3.2.P.5 Control of Drug Product", "description": "Drug product control"},
                                    {"name": "3.2.P.6 Reference Standards or Materials", "description": "Reference standards"},
                                    {"name": "3.2.P.7 Container Closure System", "description": "Container closure system"},
                                    {"name": "3.2.P.8 Stability", "description": "Drug product stability"}
                                ]
                            }
                        ]
                    },
                    {"name": "3.3 Literature References", "description": "Quality literature references"}
                ]
            },
            {
                "name": "Module 4 Nonclinical Study Reports",
                "description": "Nonclinical study documentation",
                "children": [
                    {
                        "name": "4.2 Study Reports",
                        "children": [
                            {
                                "name": "4.2.1 Pharmacology",
                                "children": [
                                    {"name": "4.2.1.1 Primary Pharmacodynamics", "description": "Primary pharmacology studies"},
                                    {"name": "4.2.1.2 Secondary Pharmacodynamics", "description": "Secondary pharmacology studies"},
                                    {"name": "4.2.1.3 Safety Pharmacology", "description": "Safety pharmacology studies"},
                                    {"name": "4.2.1.4 Pharmacodynamic Drug Interactions", "description": "Pharmacodynamic interactions"}
                                ]
                            },
                            {
                                "name": "4.2.2 Pharmacokinetics",
                                "children": [
                                    {"name": "4.2.2.1 Analytical Methods and Validation", "description": "Analytical methods"},
                                    {"name": "4.2.2.2 Absorption", "description": "Absorption studies"},
                                    {"name": "4.2.2.3 Distribution", "description": "Distribution studies"},
                                    {"name": "4.2.2.4 Metabolism", "description": "Metabolism studies"},
                                    {"name": "4.2.2.5 Excretion", "description": "Excretion studies"},
                                    {"name": "4.2.2.6 Pharmacokinetic Drug Interactions", "description": "PK interactions"},
                                    {"name": "4.2.2.7 Other Pharmacokinetic Studies", "description": "Other PK studies"}
                                ]
                            },
                            {
                                "name": "4.2.3 Toxicology",
                                "children": [
                                    {"name": "4.2.3.1 Single-Dose Toxicity", "description": "Single-dose toxicity"},
                                    {"name": "4.2.3.2 Repeat-Dose Toxicity", "description": "Repeat-dose toxicity"},
                                    {"name": "4.2.3.3 Genotoxicity", "description": "Genotoxicity studies"},
                                    {"name": "4.2.3.4 Carcinogenicity", "description": "Carcinogenicity studies"},
                                    {"name": "4.2.3.5 Reproductive and Developmental Toxicity", "description": "Reproductive toxicity"},
                                    {"name": "4.2.3.6 Local Tolerance", "description": "Local tolerance studies"},
                                    {"name": "4.2.3.7 Other Toxicity Studies", "description": "Other toxicity studies"}
                                ]
                            }
                        ]
                    },
                    {"name": "4.3 Literature References", "description": "Nonclinical literature references"}
                ]
            },
            {
                "name": "Module 5 Clinical Study Reports",
                "description": "Clinical study documentation",
                "children": [
                    {"name": "5.2 Tabular Listing of all Clinical Studies", "description": "Clinical study listings"},
                    {
                        "name": "5.3 Clinical Study Reports and Related Information",
                        "children": [
                            {
                                "name": "5.3.1 Reports of Biopharmaceutic Studies",
                                "children": [
                                    {"name": "5.3.1.1 Bioavailability (BA) Study Reports", "description": "Bioavailability studies"},
                                    {"name": "5.3.1.2 Comparative BA and BE Study Reports", "description": "Comparative BA/BE studies"},
                                    {"name": "5.3.1.3 In Vitro - In Vivo Correlation", "description": "IVIVC studies"},
                                    {"name": "5.3.1.4 Bioanalytical Methods", "description": "Bioanalytical methods"}
                                ]
                            },
                            {
                                "name": "5.3.2 Reports of Studies Pertinent to Pharmacokinetics",
                                "children": [
                                    {"name": "5.3.2.1 Plasma Protein Binding", "description": "Plasma protein binding"},
                                    {"name": "5.3.2.2 Hepatic Metabolism and Drug Interaction", "description": "Hepatic metabolism"},
                                    {"name": "5.3.2.3 Other Human Biomaterials", "description": "Other biomaterial studies"}
                                ]
                            },
                            {
                                "name": "5.3.3 Reports of Human Pharmacokinetic Studies",
                                "children": [
                                    {"name": "5.3.3.1 Healthy Subject PK", "description": "Healthy subject PK"},
                                    {"name": "5.3.3.2 Patient PK", "description": "Patient PK studies"},
                                    {"name": "5.3.3.3 Intrinsic Factor PK", "description": "Intrinsic factor PK"},
                                    {"name": "5.3.3.4 Extrinsic Factor PK", "description": "Extrinsic factor PK"},
                                    {"name": "5.3.3.5 Population PK", "description": "Population PK"}
                                ]
                            },
                            {
                                "name": "5.3.4 Reports of Human Pharmacodynamic Studies",
                                "children": [
                                    {"name": "5.3.4.1 Healthy Subject PD", "description": "Healthy subject PD"},
                                    {"name": "5.3.4.2 Patient PD", "description": "Patient PD studies"}
                                ]
                            },
                            {
                                "name": "5.3.5 Reports of Efficacy and Safety Studies",
                                "children": [
                                    {"name": "5.3.5.1 Controlled Clinical Studies", "description": "Controlled studies"},
                                    {"name": "5.3.5.2 Uncontrolled Clinical Studies", "description": "Uncontrolled studies"},
                                    {"name": "5.3.5.3 Analyses from Multiple Studies", "description": "Multi-study analyses"},
                                    {"name": "5.3.5.4 Other Study Reports", "description": "Other clinical reports"}
                                ]
                            }
                        ]
                    },
                    {"name": "5.4 Literature References", "description": "Clinical literature references"}
                ]
            }
        ]
    }
    
    # Save to JSON file
    with open(CTD_STRUCTURE_FILE, 'w') as f:
        json.dump(complete_ctd_structure, f, indent=2)
    
    print(f"Saved complete CTD structure to: {CTD_STRUCTURE_FILE}")
    
    # Create the folder structure WITHOUT README files
    total_folders = create_folder_structure(complete_ctd_structure, OUTPUT_FOLDER)
    
    print(f"\nCreated {total_folders} CTD folders in: {OUTPUT_FOLDER}")
    print("=" * 60)
    
    # Show structure summary
    show_structure_summary(OUTPUT_FOLDER)
    
    return total_folders

def create_folder_structure(node, base_path):
    """Recursively create folder structure from CTD definition"""
    folder_count = 0
    
    if not isinstance(node, dict):
        return folder_count
    
    node_name = node.get("name", "")
    if not node_name:
        return folder_count
    
    # Clean folder name (remove invalid characters)
    folder_name = clean_folder_name(node_name)
    
    # Create folder path
    folder_path = os.path.join(base_path, folder_name)
    
    # Create the folder
    os.makedirs(folder_path, exist_ok=True)
    folder_count += 1
    
    # REMOVED: Don't create README files
    
    # Process children
    children = node.get("children", [])
    if children and isinstance(children, list):
        for child in children:
            folder_count += create_folder_structure(child, folder_path)
    
    return folder_count

def clean_folder_name(name):
    """Clean folder name by removing invalid characters"""
    # Remove invalid characters for Windows/Linux
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '-')
    
    # Remove multiple spaces and trim
    name = ' '.join(name.split())
    
    return name

def show_structure_summary(base_path):
    """Show summary of created structure"""
    print("\nCTD STRUCTURE SUMMARY:")
    print("=" * 60)
    
    modules = []
    total_folders = 0
    
    for root, dirs, files in os.walk(base_path):
        level = root.replace(base_path, '').count(os.sep)
        
        if level == 0:
            continue
        
        folder_name = os.path.basename(root)
        
        if level == 1 and folder_name.startswith("Module"):
            modules.append(folder_name)
        
        if dirs or files:
            total_folders += 1
    
    print(f"Total Modules: {len(modules)}")
    for i, module in enumerate(modules, 1):
        print(f"   {i}. {module}")
    
    print(f"\nTotal Folders Created: {total_folders}")
    print(f"Location: {os.path.abspath(base_path)}")
    
    # Show folder tree (first 3 levels)
    print("\nFOLDER TREE (First 3 levels):")
    print_tree(base_path, max_depth=3)

def print_tree(start_path, prefix="", is_last=True, max_depth=3, current_depth=0):
    """Print folder tree structure with folder icons"""
    if current_depth >= max_depth:
        return
    
    items = []
    try:
        items = [item for item in os.listdir(start_path) if os.path.isdir(os.path.join(start_path, item))]
    except:
        return
    
    items.sort()
    
    for i, item in enumerate(items):
        is_last_item = i == len(items) - 1
        
        if current_depth == 0:
            # Root level - show folder icon
            connector = "📁 "
        else:
            # Subfolders
            if is_last_item:
                connector = "└── 📁 "
            else:
                connector = "├── 📁 "
        
        print(f"{prefix}{connector}{item}")
        
        # Create new prefix for next level
        if is_last_item:
            new_prefix = prefix + "    "
        else:
            new_prefix = prefix + "│   "
        
        print_tree(os.path.join(start_path, item), new_prefix, is_last_item, max_depth, current_depth + 1)

def main():
    """Main function"""
    print("=" * 60)
    print("CTD STRUCTURE BUILDER - CREATE COMPLETE FOLDER STRUCTURE")
    print("=" * 60)
    
    # Ask for confirmation
    response = input("\nThis will create the complete CTD folder structure.\nDo you want to proceed? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Operation cancelled.")
        return
    
    # Clear existing organized_ctd if exists
    if os.path.exists(OUTPUT_FOLDER):
        print(f"\n{OUTPUT_FOLDER} already exists.")
        response = input("Delete and recreate? (yes/no): ")
        
        if response.lower() in ['yes', 'y']:
            shutil.rmtree(OUTPUT_FOLDER)
            print(f"Deleted existing {OUTPUT_FOLDER}")
        else:
            print("Operation cancelled.")
            return
    
    # Create the structure
    total_folders = create_complete_ctd_structure()
    
    print(f"\nCTD structure creation complete!")
    print(f"{total_folders} folders created in {OUTPUT_FOLDER}")
    print(f"CTD definition saved to {CTD_STRUCTURE_FILE}")
    
    print("\nNEXT STEPS:")
    print("1. Add your PDF documents to 'documents_to_organize' folder")
    print("2. Run: python organize_documents.py")
    print("3. Files will be automatically placed in the correct CTD folders")
    print("=" * 60)

if __name__ == "__main__":
    main()