#!/usr/bin/env python3
# pylint: disable=C0303,C0301
"""
Enhanced Knights of Columbus Directory Generator

This script generates both Word and PDF documents from the Oklahoma Knights directory database.
Features improved table formatting and direct PDF generation.

Required packages:
pip install reportlab sqlite3 pillow

Usage:
python knights_enhanced_generator.py
python knights_enhanced_generator.py --database /path/to/db.db
"""

import sqlite3
import os
import argparse
from datetime import datetime

# PDF imports
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

class KnightsDirectoryGenerator:
    """Class to represent all functions and data for generating the KofC database"""

    def __init__(self, db_path="ok_knights_directory.db", image_path="knights_logo.jpg"):
        self.db_path = db_path
        self.image_path = image_path
        self.pdf_story = []
        self.pdf_styles = getSampleStyleSheet()
        self.setup_pdf_styles()

        self.state_abbv = {
            'oklahoma': 'OK',
            'texas': 'TX',
            'colorado': 'CO',
            '': ''
        }

    def setup_pdf_styles(self):
        """Setup custom PDF styles"""
        # Title style - larger for title page
        self.pdf_styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.pdf_styles['Title'],
            fontSize=28,
            spaceAfter=40,
            spaceBefore=40,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        ))

        # Subtitle style for title page
        self.pdf_styles.add(ParagraphStyle(
            name='SubTitle',
            parent=self.pdf_styles['Normal'],
            fontSize=16,
            spaceAfter=30,
            spaceBefore=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica'
        ))

        # Section header style
        self.pdf_styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.pdf_styles['Heading1'],
            fontSize=18,
            spaceAfter=10,
            spaceBefore=0,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))

        # Officer role style
        self.pdf_styles.add(ParagraphStyle(
            name='OfficerRole',
            parent=self.pdf_styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        ))

        # Center style
        self.pdf_styles.add(ParagraphStyle(
            name='CenterNormal',
            parent=self.pdf_styles['Normal'],
            alignment=TA_CENTER
        ))

        # Right style
        self.pdf_styles.add(ParagraphStyle(
            name='RightNormal',
            parent=self.pdf_styles['Normal'],
            alignment=TA_RIGHT
        ))

        # Add TOC styles at the end
        self.pdf_styles.add(ParagraphStyle(
        name='TOCHeading',
        parent=self.pdf_styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        spaceBefore=10,
        alignment=TA_CENTER,
        textColor=colors.darkblue
        ))

        self.pdf_styles.add(ParagraphStyle(
            name='NoBreakNormal',
            parent=self.pdf_styles['Normal'],
            spaceBefore=20,
            alignment=TA_LEFT,
            wordWrap='LTR',  # Left-to-right word wrapping
            splitLongWords=0,  # Don't split long words
        ))

    def create_title_page(self):
        """Create a full title page with image"""
        title_elements = []

        # Add main title
        title_elements.append(Paragraph("Oklahoma Knights of Columbus", self.pdf_styles['CustomTitle']))
        title_elements.append(Paragraph("State Directory", self.pdf_styles['CustomTitle']))

        # Add image if it exists
        if os.path.exists(self.image_path):
            try:
                # Create image - adjust size as needed
                img = Image(self.image_path)
                
                # Scale image to fit nicely on page (max 4 inches wide or high)
                img_width, img_height = img.drawWidth, img.drawHeight
                max_size = 4 * inch
                
                if img_width > max_size or img_height > max_size:
                    if img_width > img_height:
                        # Landscape image - scale by width
                        scale_factor = max_size / img_width
                    else:
                        # Portrait image - scale by height
                        scale_factor = max_size / img_height
                    
                    img.drawWidth = img_width * scale_factor
                    img.drawHeight = img_height * scale_factor
                
                title_elements.append(Spacer(1, 30))
                title_elements.append(img)
                title_elements.append(Spacer(1, 300))
                print(f"Added image: {self.image_path}")
                
            except FileNotFoundError as e:
                print(f"Warning: Could not load image {self.image_path}: {e}")
                title_elements.append(Spacer(1, 60))
        else:
            print(f"Image file not found: {self.image_path}")
            title_elements.append(Spacer(1, 60))
        
        # Add current year
        current_year = datetime.now().year
        next_year = current_year + 1
        title_elements.append(Paragraph(f"{current_year}-{next_year}", self.pdf_styles['SubTitle']))
        
        # Add page break after title page
        title_elements.append(PageBreak())
        
        return title_elements

    def create_pdf_officer_table(self, officer_data):
        """Create a PDF table for officers"""
        data = [
            # Row 1: Role (spanning all columns)
            [
                Paragraph(officer_data['role'], self.pdf_styles['OfficerRole'])
            ],
            # Row 2: Details
            [
                Paragraph(officer_data['full_name'], self.pdf_styles['Normal']),
                Paragraph(officer_data['wife'], self.pdf_styles['Normal']),
                Paragraph(officer_data['council'], self.pdf_styles['Normal']),
                Paragraph(officer_data['phone'], self.pdf_styles['RightNormal'])
            ],
            # Row 3: Address
            [
                Paragraph(officer_data['address'], self.pdf_styles['Normal']),
                '', '', ''
            ],
            # Row 4: City/State/Zip and Email
            [
                Paragraph(officer_data['city_state_zip'], self.pdf_styles['Normal']),
                '',
                Paragraph(officer_data['email'], self.pdf_styles['RightNormal']),
                ''
            ]
        ]
        
        table = Table(data, 
                      colWidths=[2.2*inch, 1.0*inch, 1.0*inch, 1.8*inch],
                      rowHeights=[0.3*inch, 0.175*inch, 0.175*inch, 0.175*inch])
        
        # Table styling (no borders)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('SPAN', (0, 0), (-1, 0)),  # Span role across all columns
            ('SPAN', (0, 2), (1, 2)),   # Span address across 2 columns
            ('SPAN', (0, 3), (1, 3)),   # Span city/state/zip across 2 columns
            ('SPAN', (2, 3), (3, 3)),   # Span email across 2 columns
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return KeepTogether(table)

    def create_pdf_dd_table(self, dd_data):
        """Create a PDF table for district deputies (portrait format)"""
        councils_text = '<br />'.join(dd_data['councils'])
        
        data = [
            [
                Paragraph(f"<b>{dd_data['number']}</b>", self.pdf_styles['Normal']),
                Paragraph(f"{dd_data['district_deputy']}<br/>{dd_data['address']}<br/>{dd_data['city_state_zip']}", self.pdf_styles['CenterNormal']),
                Paragraph(dd_data['email'], self.pdf_styles['CenterNormal']),
                Paragraph(dd_data['phone'], self.pdf_styles['CenterNormal']),
                Paragraph(councils_text, self.pdf_styles['CenterNormal'])
            ]
        ]
        
        # Portrait-friendly column widths
        # SUM MUST REMAIN <= 7.5
        table = Table(data, colWidths=[0.5*inch, 2.0*inch, 2.25*inch, 1.25*inch, 2.0*inch])
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (2, 3), (3, 3)),   # Span email across 2 columns
        ]))
        
        return KeepTogether(table)

    def create_pdf_programdirector_table(self, officer_data):
        """Create a PDF table for program directors and chairman"""
        data = [
            # Row 1: Role (spanning all columns)
            [
                Paragraph(officer_data['role'], self.pdf_styles['OfficerRole'])
            ],
            # Row 2: Details
            [
                Paragraph(officer_data['full_name'], self.pdf_styles['Normal']),
                Paragraph(officer_data['wife'], self.pdf_styles['Normal']),
                Paragraph(officer_data['council'], self.pdf_styles['Normal']),
                Paragraph(officer_data['phone'], self.pdf_styles['RightNormal'])
            ],
            # Row 3: Address
            [
                Paragraph(officer_data['address'], self.pdf_styles['Normal'])
            ],
            # Row 4: City/State/Zip and Email
            [
                Paragraph(officer_data['city_state_zip'], self.pdf_styles['Normal']),
                '',
                Paragraph(officer_data['email'], self.pdf_styles['RightNormal']),
                ''
            ]
        ]
        
        table = Table(data, 
                      colWidths=[2.2*inch, 1.0*inch, 1.0*inch, 1.8*inch],
                      rowHeights=[0.3*inch, 0.175*inch, 0.175*inch, 0.175*inch])
        
        # Table styling (no borders)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('SPAN', (0, 0), (-1, 0)),  # Span role across all columns
            ('SPAN', (0, 2), (2, 2)),   # Span address across 3 columns
            ('SPAN', (0, 3), (1, 3)),   # Span city/state/zip across 2 columns
            ('SPAN', (2, 3), (3, 3)),   # Span email across 2 columns
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return KeepTogether(table)
    
    def create_pdf_agents_table(self, agent):
        """Create a PDF table for all of the agents"""
        formatted_councils = agent['councils_represented'].replace(',', ', ')#'&nbsp;')
        # Format the councils text to only create new lines between council numbers

        data = [
            # Row 1: Role (spanning all columns, may have multiple entries)
            [
                Paragraph(agent['role'], self.pdf_styles['OfficerRole'])
            ],
            [
                Paragraph(agent['name'], self.pdf_styles['Normal']),
                Paragraph(agent['wife'], self.pdf_styles['CenterNormal']),
                Paragraph(agent['council'], self.pdf_styles['CenterNormal']),
                Paragraph(agent['phone'], self.pdf_styles['RightNormal'])
            ],
            [
                Paragraph(agent['address'], self.pdf_styles['Normal']),
                '',
                Paragraph(agent['email'], self.pdf_styles['RightNormal']),
                ''
            ],
            [
                Paragraph(f"{agent['city']}, {agent['state']} {agent['zip']}"),
            ],
            [
                Paragraph(f"<b>Councils:</b> {formatted_councils}", self.pdf_styles['NoBreakNormal']),
            ]
        ]

        table = Table(data, 
                      colWidths=[2.2*inch, 1.0*inch, 1.0*inch, 1.8*inch],
                      rowHeights=[0.2*inch, 0.2*inch, 0.175*inch, 0.175*inch, 0.3*inch])
        
        # Table styling (no borders)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('SPAN', (0, 0), (-1, 0)),  # Span role across all columns
            ('SPAN', (0, 2), (2, 2)),   # Span address across 2 columns
            ('SPAN', (0, 4), (2, 4)),   # Span councils across 3 columns
            ('SPAN', (2, 2), (3, 2)),   # Span email across 2 columns
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return KeepTogether(table)

    def _get_state_officers_data(self):
        """Query database for state officers"""
        if not os.path.exists(self.db_path):
            print(f"Database file not found: {self.db_path}")
            return self.get_sample_data()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM StateOfficerView"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            officers = []
            for row in rows:
                officer = {
                    'full_name': row[0] or '[ERROR]',
                    'wife': row[1] or '',
                    'address': row[2] or '[NO DATA]',
                    'city_state_zip': row[3] or '[NO DATA]',
                    'phone': self._format_phone(row[4]),
                    'email': row[5] or '[NO DATA]',
                    'council': f"{row[6]}" if row[6] else '',
                    'role': row[8] or '[ERROR]'
                }
                officers.append(officer)
            
            conn.close()
            return officers
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return self.get_sample_data()

    def _get_dd_data(self):
        """Query database for district deputies"""
        if not os.path.exists(self.db_path):
            print(f"Database file not found: {self.db_path}")
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM DistrictsView ORDER BY CAST(number AS INTEGER)"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            dds = []
            for row in rows:
                address = row[2].split('|') if row[2] else ['', '', '', '']
                # Ensure we have at least 4 elements for address
                while len(address) < 4:
                    address.append('')
                
                councils = row[6].split('|') if row[6] else []
                
                dd = {
                    'number': str(row[0]) or '[ERROR]',
                    'district_deputy': row[1] or '[VACANT]',
                    'address': address[0] or '',
                    'city_state_zip': f"{address[1]}, {self.state_abbv[str.lower(address[2])]} {address[3]}".strip(' ,'),
                    'phone': self._format_phone(row[3]) or '',
                    'email': row[4] or '',
                    'home_council': str(row[5]) or '',
                    'councils': councils
                }
                dds.append(dd)
            
            conn.close()
            return dds
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def _get_program_director_data(self):
        """Query database for state officers"""
        if not os.path.exists(self.db_path):
            print(f"Database file not found: {self.db_path}")
            return self.get_sample_data()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM ProgramDirectorView"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            officers = []
            for row in rows:
                officer = {
                    'full_name': row[0] or '[VACANT]',
                    'wife': row[1] or '',
                    'address': row[2] or '[NO DATA]',
                    'city_state_zip': row[3] or '[NO DATA]',
                    'phone': self._format_phone(row[4]),
                    'email': row[5] or '[NO DATA]',
                    'council': f"{row[6]}" if row[6] else '[NO DATA]',
                    'role': row[8] or '[ERROR]'
                }
                officers.append(officer)
            
            conn.close()
            return officers
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return self.get_sample_data()
        
    def _get_agent_data(self):
        """Query database for state officers"""
        if not os.path.exists(self.db_path):
            print(f"Database file not found: {self.db_path}")
            return self.get_sample_data()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM AgentsView"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            agents = []
            for row in rows:
                agent = {
                    'name': row[0] or '[ERROR]',
                    'wife': row[1] or '',
                    'email': row[2] or '[ERROR]',
                    'council': str(row[3]) or '[ERROR]',
                    'phone': self._format_phone(row[4]) or '[ERROR]',
                    'councils_represented': row[5] or '',
                    'role': row[6] or '[ERROR]',
                    'address': row[7] or '',
                    'city': row[8] or '',
                    'state': self.state_abbv[str.lower(row[9])] or '',
                    'zip': row[10] or ''
                }
                agents.append(agent)
            
            conn.close()
            return agents
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return self.get_sample_data()

    def _format_phone(self, phone):
        """Format phone number"""
        if not phone:
            return ''
        
        digits = ''.join(filter(str.isdigit, str(phone)))
        
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            return str(phone)

    def get_sample_data(self):
        """Sample data for testing"""
        return [
            {
                'role': 'STATE DEPUTY',
                'full_name': 'John Doe',
                'wife': 'Jane Doe',
                'council': 'Council 1234',
                'phone': '(405) 555-0123',
                'address': '123 Main Street',
                'city_state_zip': 'Oklahoma City, OK 73101',
                'email': 'john.doe@email.com'
            }
        ]

    def generate_document(self, output_base):
        """Generate PDF document with simple linked TOC"""
        print("Generating PDF document with simple TOC...")
        
        margin_factor = 1.0

        # Generate PDF document with timestamp        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"{output_base}_{timestamp}.pdf"

        doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                            rightMargin=margin_factor*inch, leftMargin=margin_factor*inch,
                            topMargin=margin_factor*inch, bottomMargin=margin_factor*inch)
        
        story = []
        
        # Add title page
        story.extend(self.create_title_page())
        
        # Add simple TOC
        story.append(Paragraph("Table of Contents", self.pdf_styles['TOCHeading']))
        story.append(Spacer(1, 30))
        
        # Manual TOC entries with links
        story.append(Paragraph('<link href="#state_officers" color="blue">State Council Officers</link>', self.pdf_styles['Normal']))
        story.append(Spacer(1, 8))
        story.append(Paragraph('<link href="#district_deputies" color="blue">District Deputies</link>', self.pdf_styles['Normal']))
        story.append(Spacer(1, 8))
        story.append(Paragraph('<link href="#program_directors" color="blue">Program Directors and Chairmen</link>', self.pdf_styles['Normal']))
        story.append(Spacer(1, 8))
        story.append(Paragraph('<link href="#agents" color="blue">Insurance Agents</link>', self.pdf_styles['Normal']))
        story.append(PageBreak())
        
        # Officers section with anchor
        officers = self._get_state_officers_data()
        if officers:
            story.append(Paragraph('<a name="state_officers"/>State Council Officers', self.pdf_styles['SectionHeader']))
            story.append(Paragraph('Official State Council Website: <link href="https://www.okkofc.org">www.okkofc.org</link>',
                                   self.pdf_styles['CenterNormal']))
            story.append(Paragraph('State forms submittal email: <link href=mailto:okkofcsubmit@gmail.com">okkofcsubmit@gmail.com</link>',
                                   self.pdf_styles['CenterNormal']))
            story.append(Spacer(1, 5))
            
            for officer in officers:
                print(f"Adding {officer['role']}: {officer['full_name']}")
                story.append(self.create_pdf_officer_table(officer))
                story.append(Spacer(1, 12))
            
            story.append(PageBreak())
        
        # District Deputies section with anchor
        dds = self._get_dd_data()
        if dds:
            story.append(Paragraph('<a name="district_deputies"/>District Deputies', self.pdf_styles['SectionHeader']))
            story.append(Spacer(1, 12))
            
            for dd in dds:
                print(f"Adding District {dd['number']}: {dd['district_deputy']}")
                story.append(self.create_pdf_dd_table(dd))
                story.append(Spacer(1, 8))
            
            story.append(PageBreak())
        
        # Program Directors Section with anchor
        p_directors = self._get_program_director_data()
        if p_directors:
            story.append(Paragraph('<a name="program_directors"/>Program Directors and Chairmen', self.pdf_styles['SectionHeader']))
            story.append(Spacer(1, 5))

            for director in p_directors:
                print(f"Adding {director['role']}: {director['full_name']}")
                story.append(self.create_pdf_programdirector_table(director))
                story.append(Spacer(1, 12))

        story.append(PageBreak())

        # Insurance Agents Section with anchor
        agents =self._get_agent_data()
        if agents:
            story.append(Paragraph('<a name="agents"/>Insurance Agents',
                                   self.pdf_styles['SectionHeader']))
            story.append(Spacer(1,5))

            for agent in agents:
                print(f"Adding agent {agent['name']}")
                story.append(self.create_pdf_agents_table(agent))
                story.append(Spacer(1, 12))

            story.append(PageBreak())

        # TODO Past State Deputies Section with Anchor
        # | TERM | NAME    | ----- | COUNCIL | PHONE |
        # | ---- | ADDRESS | ----- | ------- | ----- |
        # | ---- | C/S/Z   | EMAIL | ------- | ----- |

        # NO BREAK

        # TODO Widows of Past State Deputies with Anchor
        # | TERM | NAME    | ----- | COUNCIL | PHONE |
        # | ---- | ADDRESS | ----- | ------- | ----- |
        # | ---- | C/S/Z   | EMAIL | ------- | ----- |

        doc.build(story)
        print(f"PDF document saved as: {pdf_filename}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Generate Knights of Columbus Directory PDF')
    parser.add_argument('--database', default='ok_knights_directory.db',
                       help='Database file path')
    parser.add_argument('--output', default='OK_Knights_Directory',
                       help='Output filename base')
    parser.add_argument('--image', default='knights_logo.jpg',
                       help='Logo image file path')
    
    args = parser.parse_args()
    
    generator = KnightsDirectoryGenerator(args.database, args.image)
    generator.generate_document(args.output)
    
    print("\nSuccess! Directory generated as PDF")

if __name__ == "__main__":
    main()
