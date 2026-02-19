"""
Certificate Generator for SkillVerse
Generates professional completion certificates for completed orders
"""

from PIL import Image, ImageDraw, ImageFont
import io
import os
from datetime import datetime
import qrcode

class CertificateGenerator:
    """Generate professional certificates for completed services"""
    
    def __init__(self):
        self.width = 1200
        self.height = 850
        self.bg_color = '#ffffff'  # Clean white background
        self.primary_color = '#4f46e5'  # Modern indigo
        self.secondary_color = '#818cf8'  # Light indigo
        self.accent_color = '#f59e0b'  # Warm amber/gold
        self.text_color = '#1e293b'  # Dark slate
        self.light_text = '#64748b'  # Light slate
        
    def generate_certificate(self, buyer_name, service_title, completion_date, order_id, instructor_name):
        """
        Generate a modern, elegant certificate with unique SkillVerse branding
        
        Args:
            buyer_name: Name of the person who completed the service
            service_title: Title of the service completed
            completion_date: Date of completion
            order_id: Order ID for reference
            instructor_name: Name of the instructor/provider
            
        Returns:
            BytesIO: Certificate image as bytes
        """
        # Create image with white background
        img = Image.new('RGB', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw modern gradient border effect with shadow
        border_width = 10
        
        # Shadow effect
        shadow_offset = 3
        draw.rectangle([border_width + shadow_offset, border_width + shadow_offset, 
                       self.width - border_width + shadow_offset, self.height - border_width + shadow_offset], 
                      outline='#e2e8f0', width=2)
        
        # Outer border - primary color with gradient effect
        for i in range(border_width):
            alpha = i / border_width
            draw.rectangle([border_width - i, border_width - i, 
                           self.width - border_width + i, self.height - border_width + i], 
                          outline=self.primary_color, width=1)
        
        # Inner decorative border - accent color
        inner_offset = border_width + 20
        draw.rectangle([inner_offset, inner_offset, self.width-inner_offset, self.height-inner_offset], 
                      outline=self.accent_color, width=3)
        
        # Double line effect
        draw.rectangle([inner_offset + 5, inner_offset + 5, 
                       self.width-inner_offset - 5, self.height-inner_offset - 5], 
                      outline=self.secondary_color, width=1)
        
        # Top accent bar with gradient effect (improved)
        gradient_height = 100
        for i in range(gradient_height):
            alpha = i / gradient_height
            # Smooth gradient from primary to light
            r = int(79 + (248 - 79) * alpha)
            g = int(70 + (250 - 70) * alpha)
            b = int(229 + (252 - 229) * alpha)
            draw.rectangle([inner_offset, inner_offset + i, self.width-inner_offset, inner_offset + i + 1], 
                          fill=f'#{r:02x}{g:02x}{b:02x}')
        
        # Modern corner accents (larger circles with glow effect)
        corner_radius = 15
        corner_offset = border_width + 10
        
        # Draw glow effect for corners
        for glow_r in range(corner_radius + 5, corner_radius, -1):
            glow_alpha = (corner_radius + 5 - glow_r) / 5
            glow_color = f'#{int(245 + 10 * glow_alpha):02x}{int(158 + 97 * glow_alpha):02x}{int(11 + 218 * glow_alpha):02x}'
            
            # Top-left
            draw.ellipse([corner_offset-glow_r, corner_offset-glow_r, 
                         corner_offset+glow_r, corner_offset+glow_r], 
                        outline=glow_color, width=1)
            # Top-right
            draw.ellipse([self.width-corner_offset-glow_r, corner_offset-glow_r, 
                         self.width-corner_offset+glow_r, corner_offset+glow_r], 
                        outline=glow_color, width=1)
            # Bottom-left
            draw.ellipse([corner_offset-glow_r, self.height-corner_offset-glow_r, 
                         corner_offset+glow_r, self.height-corner_offset+glow_r], 
                        outline=glow_color, width=1)
            # Bottom-right
            draw.ellipse([self.width-corner_offset-glow_r, self.height-corner_offset-glow_r, 
                         self.width-corner_offset+glow_r, self.height-corner_offset+glow_r], 
                        outline=glow_color, width=1)
        
        # Main corner circles
        # Top-left
        draw.ellipse([corner_offset-corner_radius, corner_offset-corner_radius, 
                     corner_offset+corner_radius, corner_offset+corner_radius], 
                    fill=self.accent_color)
        # Top-right
        draw.ellipse([self.width-corner_offset-corner_radius, corner_offset-corner_radius, 
                     self.width-corner_offset+corner_radius, corner_offset+corner_radius], 
                    fill=self.accent_color)
        # Bottom-left
        draw.ellipse([corner_offset-corner_radius, self.height-corner_offset-corner_radius, 
                     corner_offset+corner_radius, self.height-corner_offset+corner_radius], 
                    fill=self.accent_color)
        # Bottom-right
        draw.ellipse([self.width-corner_offset-corner_radius, self.height-corner_offset-corner_radius, 
                     self.width-corner_offset+corner_radius, self.height-corner_offset+corner_radius], 
                    fill=self.accent_color)
        
        # Try to load fonts, fallback to default if not available
        try:
            brand_font = ImageFont.truetype("arialbd.ttf", 20)
            title_font = ImageFont.truetype("arialbd.ttf", 56)
            subtitle_font = ImageFont.truetype("arial.ttf", 22)
            name_font = ImageFont.truetype("arialbd.ttf", 68)
            text_font = ImageFont.truetype("arial.ttf", 24)
            small_font = ImageFont.truetype("arial.ttf", 18)
            tiny_font = ImageFont.truetype("arial.ttf", 14)
        except:
            # Fallback to default font
            brand_font = ImageFont.load_default()
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            name_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            tiny_font = ImageFont.load_default()
        
        # SkillVerse logo/brand at top with decorative elements
        brand_text = "★ SKILLVERSE ★"
        brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
        brand_width = brand_bbox[2] - brand_bbox[0]
        brand_x = (self.width - brand_width) / 2
        
        # Brand background
        draw.rectangle([brand_x - 30, 135, brand_x + brand_width + 30, 165], 
                      fill='#eef2ff', outline=self.primary_color, width=2)
        draw.text((brand_x, 140), brand_text, fill=self.primary_color, font=brand_font)
        
        # Decorative lines under brand (extended)
        draw.line([(self.width/2 - 80, 175), (self.width/2 + 80, 175)], 
                 fill=self.accent_color, width=4)
        # Small accent dots
        for dot_x in [self.width/2 - 90, self.width/2 + 90]:
            draw.ellipse([dot_x - 3, 172, dot_x + 3, 178], fill=self.accent_color)
        
        # Main title with shadow effect
        title_text = "CERTIFICATE"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) / 2
        
        # Shadow
        draw.text((title_x + 2, 192), title_text, fill='#cbd5e1', font=title_font)
        # Main text
        draw.text((title_x, 190), title_text, fill=self.primary_color, font=title_font)
        
        # Subtitle
        subtitle_text = "OF COMPLETION"
        subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        draw.text(((self.width - subtitle_width) / 2, 250), subtitle_text, 
                 fill=self.text_color, font=subtitle_font)
        
        # Decorative line under title
        draw.line([(self.width/2 - 200, 280), (self.width/2 + 200, 280)], 
                 fill=self.secondary_color, width=2)
        
        # Subtitle
        subtitle_text = "This is to certify that"
        subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        draw.text(((self.width - subtitle_width) / 2, 295), subtitle_text, 
                 fill=self.light_text, font=subtitle_font)
        
        # Buyer Name (large and prominent with better styling)
        name_bbox = draw.textbbox((0, 0), buyer_name, font=name_font)
        name_width = name_bbox[2] - name_bbox[0]
        name_x = (self.width - name_width) / 2
        name_y = 335
        
        # Name background with gradient
        name_padding = 25
        name_box_y1 = name_y - 12
        name_box_y2 = name_y + 78
        
        # Gradient background for name
        for i in range(int(name_box_y2 - name_box_y1)):
            alpha = i / (name_box_y2 - name_box_y1)
            r = int(248 + (241 - 248) * alpha)
            g = int(250 + (245 - 250) * alpha)
            b = int(252 + (249 - 252) * alpha)
            draw.rectangle([name_x - name_padding, name_box_y1 + i, 
                           name_x + name_width + name_padding, name_box_y1 + i + 1], 
                          fill=f'#{r:02x}{g:02x}{b:02x}')
        
        # Border for name box
        draw.rectangle([name_x - name_padding, name_box_y1, 
                       name_x + name_width + name_padding, name_box_y2], 
                      outline=self.primary_color, width=3)
        
        draw.text((name_x, name_y), buyer_name, fill=self.primary_color, font=name_font)
        
        # Decorative underline with accent (thicker and more prominent)
        line_y = name_y + 95
        draw.line([(name_x - 40, line_y), (name_x + name_width + 40, line_y)], 
                 fill=self.accent_color, width=5)
        # Small decorative elements
        draw.ellipse([name_x - 50, line_y - 5, name_x - 40, line_y + 5], fill=self.accent_color)
        draw.ellipse([name_x + name_width + 40, line_y - 5, name_x + name_width + 50, line_y + 5], 
                    fill=self.accent_color)
        
        # Achievement text
        achievement_text = "has successfully completed"
        achievement_bbox = draw.textbbox((0, 0), achievement_text, font=text_font)
        achievement_width = achievement_bbox[2] - achievement_bbox[0]
        draw.text(((self.width - achievement_width) / 2, 455), achievement_text, 
                 fill=self.text_color, font=text_font)
        
        # Service Title (highlighted box with better styling)
        service_y = 495
        # Wrap service title if too long
        max_service_width = 900
        service_lines = self._wrap_text(service_title, text_font, draw, max_service_width)
        
        for idx, line in enumerate(service_lines):
            line_bbox = draw.textbbox((0, 0), line, font=text_font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (self.width - line_width) / 2
            
            # Background for service title (improved)
            if idx == 0:
                # Gradient background
                box_height = 40
                for i in range(box_height):
                    alpha = i / box_height
                    r = int(79 + (129 - 79) * alpha)
                    g = int(70 + (140 - 70) * alpha)
                    b = int(229 + (248 - 229) * alpha)
                    draw.rectangle([line_x - 30, service_y - 10 + i, 
                                   line_x + line_width + 30, service_y - 10 + i + 1], 
                                  fill=f'#{r:02x}{g:02x}{b:02x}')
                
                # Border
                draw.rectangle([line_x - 30, service_y - 10, 
                               line_x + line_width + 30, service_y + 30], 
                              outline=self.primary_color, width=2)
                draw.text((line_x, service_y - 5), line, fill='#ffffff', font=text_font)
            else:
                draw.text((line_x, service_y), line, fill=self.primary_color, font=text_font)
            service_y += 40
        
        # Platform text with instructor
        platform_text = "through SkillVerse Learning Platform"
        platform_bbox = draw.textbbox((0, 0), platform_text, font=small_font)
        platform_width = platform_bbox[2] - platform_bbox[0]
        draw.text(((self.width - platform_width) / 2, service_y + 10), platform_text, 
                 fill=self.light_text, font=small_font)
        
        # Instructor section (moved down to avoid overlap)
        instructor_y = service_y + 45
        instructor_label = "Instructed by"
        instructor_label_bbox = draw.textbbox((0, 0), instructor_label, font=tiny_font)
        instructor_label_width = instructor_label_bbox[2] - instructor_label_bbox[0]
        draw.text(((self.width - instructor_label_width) / 2, instructor_y), instructor_label, 
                 fill=self.light_text, font=tiny_font)
        
        # Instructor name with icon
        instructor_display = f"👨‍🏫 {instructor_name}"
        instructor_bbox = draw.textbbox((0, 0), instructor_display, font=text_font)
        instructor_width = instructor_bbox[2] - instructor_bbox[0]
        instructor_x = (self.width - instructor_width) / 2
        
        # Background box for instructor
        draw.rectangle([instructor_x - 15, instructor_y + 18, 
                       instructor_x + instructor_width + 15, instructor_y + 50], 
                      fill='#fef3c7', outline=self.accent_color, width=2)
        draw.text((instructor_x, instructor_y + 22), instructor_display, 
                 fill=self.text_color, font=text_font)
        
        # Certificate ID section (centered, below instructor)
        cert_id_y = instructor_y + 75
        cert_id = f"CERT-{order_id:06d}"
        cert_label = "Certificate ID"
        cert_label_bbox = draw.textbbox((0, 0), cert_label, font=tiny_font)
        cert_label_width = cert_label_bbox[2] - cert_label_bbox[0]
        draw.text(((self.width - cert_label_width) / 2, cert_id_y), cert_label, 
                 fill=self.light_text, font=tiny_font)
        
        # Certificate ID box
        cert_id_bbox = draw.textbbox((0, 0), cert_id, font=text_font)
        cert_id_width = cert_id_bbox[2] - cert_id_bbox[0]
        cert_id_x = (self.width - cert_id_width) / 2
        
        draw.rectangle([cert_id_x - 20, cert_id_y + 18, 
                       cert_id_x + cert_id_width + 20, cert_id_y + 48], 
                      fill='#ede9fe', outline=self.primary_color, width=2)
        draw.text((cert_id_x, cert_id_y + 22), cert_id, 
                 fill=self.primary_color, font=text_font)
        
        # Decorative separator (moved down)
        sep_y = cert_id_y + 65
        draw.ellipse([self.width/2 - 4, sep_y - 4, self.width/2 + 4, sep_y + 4], 
                    fill=self.accent_color)
        draw.line([(self.width/2 - 150, sep_y), (self.width/2 - 15, sep_y)], 
                 fill=self.secondary_color, width=2)
        draw.line([(self.width/2 + 15, sep_y), (self.width/2 + 150, sep_y)], 
                 fill=self.secondary_color, width=2)
        
        # Bottom section with details (better alignment and spacing)
        bottom_y = sep_y + 30
        
        # Left: Date section
        date_icon_x = 180
        draw.ellipse([date_icon_x - 22, bottom_y - 22, date_icon_x + 22, bottom_y + 22], 
                    fill=self.secondary_color)
        date_emoji = "📅"
        draw.text((date_icon_x - 10, bottom_y - 14), date_emoji, font=small_font)
        
        date_label = "Date of Completion"
        draw.text((date_icon_x - 50, bottom_y + 30), date_label, 
                 fill=self.light_text, font=tiny_font)
        draw.text((date_icon_x - 40, bottom_y + 48), completion_date, 
                 fill=self.text_color, font=small_font)
        
        # Right: Order Reference
        order_icon_x = self.width - 180
        draw.ellipse([order_icon_x - 22, bottom_y - 22, order_icon_x + 22, bottom_y + 22], 
                    fill=self.secondary_color)
        order_emoji = "🎯"
        draw.text((order_icon_x - 10, bottom_y - 14), order_emoji, font=small_font)
        
        order_label = "Order Reference"
        order_label_bbox = draw.textbbox((0, 0), order_label, font=tiny_font)
        order_label_width = order_label_bbox[2] - order_label_bbox[0]
        draw.text((order_icon_x - order_label_width + 10, bottom_y + 30), order_label, 
                 fill=self.light_text, font=tiny_font)
        order_value = f"#{order_id}"
        order_value_bbox = draw.textbbox((0, 0), order_value, font=small_font)
        order_value_width = order_value_bbox[2] - order_value_bbox[0]
        draw.text((order_icon_x - order_value_width + 10, bottom_y + 48), order_value, 
                 fill=self.text_color, font=small_font)
        
        # Signature section
        sig_y = bottom_y + 90
        
        # Left signature
        sig_line_width = 180
        sig1_x = 200
        draw.line([(sig1_x, sig_y), (sig1_x + sig_line_width, sig_y)], 
                 fill=self.light_text, width=1)
        sig1_name = "Authorized Signature"
        draw.text((sig1_x + 20, sig_y + 8), sig1_name, 
                 fill=self.light_text, font=tiny_font)
        sig1_title = "SkillVerse Team"
        draw.text((sig1_x + 30, sig_y + 26), sig1_title, 
                 fill=self.text_color, font=small_font)
        
        # Center: Badge/Seal
        seal_center_x = self.width / 2
        seal_center_y = sig_y + 20
        # Outer circle
        draw.ellipse([seal_center_x - 35, seal_center_y - 35, 
                     seal_center_x + 35, seal_center_y + 35], 
                    outline=self.primary_color, width=3)
        # Inner circle
        draw.ellipse([seal_center_x - 28, seal_center_y - 28, 
                     seal_center_x + 28, seal_center_y + 28], 
                    outline=self.accent_color, width=2)
        # Star/checkmark
        check_text = "✓"
        check_bbox = draw.textbbox((0, 0), check_text, font=title_font)
        check_width = check_bbox[2] - check_bbox[0]
        check_height = check_bbox[3] - check_bbox[1]
        draw.text((seal_center_x - check_width/2, seal_center_y - check_height/2 - 8), 
                 check_text, fill=self.primary_color, font=title_font)
        
        # Right signature
        sig2_x = self.width - 200 - sig_line_width
        draw.line([(sig2_x, sig_y), (sig2_x + sig_line_width, sig_y)], 
                 fill=self.light_text, width=1)
        sig2_name = "Platform Director"
        sig2_bbox = draw.textbbox((0, 0), sig2_name, font=tiny_font)
        sig2_width = sig2_bbox[2] - sig2_bbox[0]
        draw.text((sig2_x + sig_line_width - sig2_width - 20, sig_y + 8), sig2_name, 
                 fill=self.light_text, font=tiny_font)
        sig2_title = "SkillVerse"
        sig2_title_bbox = draw.textbbox((0, 0), sig2_title, font=small_font)
        sig2_title_width = sig2_title_bbox[2] - sig2_title_bbox[0]
        draw.text((sig2_x + sig_line_width - sig2_title_width - 30, sig_y + 26), sig2_title, 
                 fill=self.text_color, font=small_font)
        
        # Footer
        footer_y = sig_y + 80
        footer_text = "This certificate validates the successful completion of the course • www.skillverse.com"
        footer_bbox = draw.textbbox((0, 0), footer_text, font=tiny_font)
        footer_width = footer_bbox[2] - footer_bbox[0]
        draw.text(((self.width - footer_width) / 2, footer_y), footer_text, 
                 fill=self.light_text, font=tiny_font)
        
        # Save to BytesIO
        img_io = io.BytesIO()
        img.save(img_io, 'PNG', quality=95)
        img_io.seek(0)
        
        return img_io
    
    def _wrap_text(self, text, font, draw, max_width):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines


# Global instance
certificate_generator = CertificateGenerator()
