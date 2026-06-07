import os

js_code = """
/**
 * OPTICAL ASTROLABE ENGINE
 * Replaces the old Indiana Jones ink sketch with a massive,
 * glowing, mathematically precise optical mechanism (Astrolabe / Lenses).
 */

class IndianaJonesEngine {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        
        this.ctx = this.canvas.getContext('2d');
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        
        // Configuration
        this.particles = [];
        this.numParticles = 100; // Gold dust
        this.time = 0;
        
        // Mouse interaction
        this.mouseX = this.width / 2;
        this.mouseY = this.height / 2;
        this.targetMouseX = this.width / 2;
        this.targetMouseY = this.height / 2;
        
        this.isRunning = true;
        
        this.init();
        this.bindEvents();
        this.loop();
    }
    
    init() {
        this.resize();
        
        // Init dust particles
        this.particles = [];
        for (let i = 0; i < this.numParticles; i++) {
            this.particles.push({
                x: Math.random() * this.width,
                y: Math.random() * this.height,
                z: Math.random() * 2 + 0.1,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 0.5,
                alpha: Math.random() * 0.5 + 0.1
            });
        }
    }
    
    bindEvents() {
        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => {
            this.targetMouseX = e.clientX;
            this.targetMouseY = e.clientY;
        });
    }
    
    resize() {
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.canvas.width = this.width;
        this.canvas.height = this.height;
    }
    
    drawAstrolabe(cx, cy) {
        const ctx = this.ctx;
        const t = this.time * 0.001;
        
        // Parallax offset based on mouse
        const dx = (this.mouseX - this.width/2) * 0.05;
        const dy = (this.mouseY - this.height/2) * 0.05;
        
        ctx.save();
        ctx.translate(cx + dx, cy + dy);
        
        // Central light glow
        const glow = ctx.createRadialGradient(0, 0, 10, 0, 0, 400);
        glow.addColorStop(0, 'rgba(207, 177, 143, 0.15)');
        glow.addColorStop(0.5, 'rgba(139, 21, 21, 0.05)');
        glow.addColorStop(1, 'rgba(0, 0, 0, 0)');
        
        ctx.globalCompositeOperation = 'screen';
        ctx.fillStyle = glow;
        ctx.beginPath();
        ctx.arc(0, 0, 500, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw majestic rotating rings
        const numRings = 7;
        for (let i = 1; i <= numRings; i++) {
            ctx.save();
            // Complex rotation: some clockwise, some counter, varying speeds
            const dir = i % 2 === 0 ? 1 : -1;
            const speed = 0.1 + (numRings - i) * 0.05;
            ctx.rotate(t * speed * dir + (i * 0.5));
            
            // 3D tilt illusion
            ctx.scale(1, 0.3 + (Math.sin(t * 0.2 + i) * 0.1 + 0.1));
            
            const radius = 100 * i + (Math.sin(t * 0.5 + i) * 20);
            
            ctx.beginPath();
            ctx.arc(0, 0, radius, 0, Math.PI * 2);
            ctx.lineWidth = i % 3 === 0 ? 3 : 1;
            
            // Premium gold/copper color
            ctx.strokeStyle = `rgba(207, 177, 143, ${0.1 + (i/numRings) * 0.2})`;
            ctx.stroke();
            
            // Add ticks to some rings
            if (i % 2 === 0) {
                const numTicks = 36 * i;
                for (let j = 0; j < numTicks; j++) {
                    const angle = (j / numTicks) * Math.PI * 2;
                    ctx.beginPath();
                    ctx.moveTo(Math.cos(angle) * radius, Math.sin(angle) * radius);
                    const tickLen = j % 10 === 0 ? 15 : 5;
                    ctx.lineTo(Math.cos(angle) * (radius - tickLen), Math.sin(angle) * (radius - tickLen));
                    ctx.strokeStyle = `rgba(207, 177, 143, 0.3)`;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }
            }
            
            ctx.restore();
        }
        
        // Light rays (Volumetric)
        const numRays = 12;
        ctx.save();
        ctx.rotate(t * 0.05);
        for (let i = 0; i < numRays; i++) {
            const angle = (i / numRays) * Math.PI * 2;
            const grad = ctx.createLinearGradient(0, 0, Math.cos(angle)*800, Math.sin(angle)*800);
            grad.addColorStop(0, 'rgba(255, 240, 200, 0.08)');
            grad.addColorStop(1, 'rgba(255, 240, 200, 0)');
            
            ctx.beginPath();
            ctx.moveTo(0, 0);
            // Triangle shape ray
            const spread = 0.1 + Math.sin(t + i)*0.05;
            ctx.lineTo(Math.cos(angle - spread)*800, Math.sin(angle - spread)*800);
            ctx.lineTo(Math.cos(angle + spread)*800, Math.sin(angle + spread)*800);
            ctx.closePath();
            ctx.fillStyle = grad;
            ctx.fill();
        }
        ctx.restore();
        
        // Sacred Geometry Core
        ctx.save();
        ctx.rotate(-t * 0.2);
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {
            const angle = (i / 6) * Math.PI * 2;
            if (i === 0) ctx.moveTo(Math.cos(angle)*80, Math.sin(angle)*80);
            else ctx.lineTo(Math.cos(angle)*80, Math.sin(angle)*80);
        }
        ctx.closePath();
        ctx.strokeStyle = 'rgba(255, 215, 150, 0.5)';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {
            const angle = ((i+0.5) / 6) * Math.PI * 2;
            if (i === 0) ctx.moveTo(Math.cos(angle)*80, Math.sin(angle)*80);
            else ctx.lineTo(Math.cos(angle)*80, Math.sin(angle)*80);
        }
        ctx.closePath();
        ctx.stroke();
        
        ctx.restore();
        
        ctx.restore();
    }
    
    updateDust() {
        this.particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy - (p.z * 0.2); // Float upwards slowly
            
            // Wrap around
            if (p.x < 0) p.x = this.width;
            if (p.x > this.width) p.x = 0;
            if (p.y < 0) p.y = this.height;
            if (p.y > this.height) p.y = 0;
            
            // Twinkle
            p.alpha = 0.1 + Math.abs(Math.sin(this.time * 0.002 * p.z)) * 0.4;
        });
    }
    
    drawDust() {
        const ctx = this.ctx;
        ctx.globalCompositeOperation = 'screen';
        
        // Mouse parallax for dust
        const dx = (this.mouseX - this.width/2) * 0.02;
        const dy = (this.mouseY - this.height/2) * 0.02;
        
        this.particles.forEach(p => {
            const px = p.x + dx * p.z;
            const py = p.y + dy * p.z;
            
            ctx.beginPath();
            ctx.arc(px, py, p.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 230, 180, ${p.alpha})`;
            ctx.fill();
        });
    }
    
    loop(timestamp) {
        if (!this.isRunning) return;
        
        this.time = timestamp || 0;
        
        // Smooth mouse
        this.mouseX += (this.targetMouseX - this.mouseX) * 0.05;
        this.mouseY += (this.targetMouseY - this.mouseY) * 0.05;
        
        // Clear background with deep dark transparent for motion blur
        this.ctx.globalCompositeOperation = 'source-over';
        this.ctx.fillStyle = 'rgba(10, 8, 7, 0.3)'; // Deep dark brown/black
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        this.drawAstrolabe(this.width * 0.7, this.height * 0.5); // Offset to the right
        this.drawAstrolabe(this.width * 0.2, this.height * 0.8); // Smaller offset to the left bottom
        
        this.updateDust();
        this.drawDust();
        
        requestAnimationFrame((t) => this.loop(t));
    }
    
    destroy() {
        this.isRunning = false;
        this.ctx.clearRect(0, 0, this.width, this.height);
    }
}

window.IndianaJonesEngine = IndianaJonesEngine;
"""

with open('IndianaJonesEngine.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
print("IndianaJonesEngine.js overwritten with Astrolabe Engine")
