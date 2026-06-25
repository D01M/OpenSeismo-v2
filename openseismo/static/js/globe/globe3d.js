/**
 * 3D Animated Globe using Three.js
 * Real-time earthquake visualization on a rotating 3D globe
 */

class Globe3D {
    constructor(containerId = 'globe-container') {
        this.container = document.getElementById(containerId);
        
        if (!this.container) {
            console.error('Globe container not found, creating...');
            this.container = document.createElement('div');
            this.container.id = containerId;
            this.container.style.width = '100%';
            this.container.style.height = '100vh';
            this.container.style.position = 'fixed';
            this.container.style.top = '0';
            this.container.style.left = '0';
            this.container.style.zIndex = '1';
            this.container.style.background = 'radial-gradient(ellipse at center, #0a0e27 0%, #000000 100%)';
            document.body.insertBefore(this.container, document.body.firstChild);
        }

        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            10000
        );
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        
        this.setup();
        this.createGlobe();
        this.createLighting();
        this.startAnimation();
        this.setupMouseControls();
        
        window.addEventListener('resize', () => this.onWindowResize());
    }

    setup() {
        // Renderer setup
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setClearColor(0x000814, 1);
        
        // Get or create globe container
        let globeContainer = document.getElementById('globe-container');
        if (!globeContainer) {
            // Create container if it doesn't exist
            globeContainer = document.createElement('div');
            globeContainer.id = 'globe-container';
            globeContainer.style.width = '100%';
            globeContainer.style.height = '100vh';
            globeContainer.style.position = 'fixed';
            globeContainer.style.top = '0';
            globeContainer.style.left = '0';
            globeContainer.style.zIndex = '1';
            globeContainer.style.background = 'radial-gradient(ellipse at center, #0a0e27 0%, #000000 100%)';
            document.body.insertBefore(globeContainer, document.body.firstChild);
        }
        
        // Append renderer to container
        globeContainer.appendChild(this.renderer.domElement);

        // Camera position
        this.camera.position.z = 2.5;

        // Raycaster for mouse interaction
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
    }

    createGlobe() {
        // Earth sphere
        const geometry = new THREE.SphereGeometry(1, 128, 128);
        
        // Create realistic Earth texture on canvas
        const canvas = document.createElement('canvas');
        canvas.width = 2048;
        canvas.height = 1024;
        const ctx = canvas.getContext('2d');
        
        // Ocean blue background
        const oceanBlue = '#1a5f8f';
        ctx.fillStyle = oceanBlue;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Add some water variation with noise
        const oceanColors = ['#1a5f8f', '#2a7fa0', '#1a4f7f'];
        for (let i = 0; i < 500; i++) {
            ctx.fillStyle = oceanColors[Math.floor(Math.random() * oceanColors.length)];
            ctx.globalAlpha = 0.3;
            ctx.fillRect(
                Math.random() * canvas.width,
                Math.random() * canvas.height,
                Math.random() * 100 + 10,
                Math.random() * 100 + 10
            );
        }
        ctx.globalAlpha = 1;
        
        // Land masses (continents) in green/brown
        const landColor = '#2d5016';
        ctx.fillStyle = landColor;
        
        // Approximate landmass positions and shapes
        const continents = [
            // North America
            { x: 0.15, y: 0.35, w: 0.12, h: 0.15 },
            // South America
            { x: 0.20, y: 0.55, w: 0.06, h: 0.12 },
            // Europe
            { x: 0.48, y: 0.30, w: 0.06, h: 0.06 },
            // Africa
            { x: 0.50, y: 0.42, w: 0.08, h: 0.15 },
            // Middle East
            { x: 0.55, y: 0.38, w: 0.05, h: 0.06 },
            // Asia
            { x: 0.60, y: 0.35, w: 0.20, h: 0.15 },
            // Australia
            { x: 0.78, y: 0.60, w: 0.06, h: 0.08 },
            // Antarctica (bottom)
            { x: 0, y: 0.85, w: 1.0, h: 0.15 },
            // Greenland
            { x: 0.35, y: 0.15, w: 0.04, h: 0.08 }
        ];
        
        continents.forEach(continent => {
            ctx.fillRect(
                continent.x * canvas.width,
                continent.y * canvas.height,
                continent.w * canvas.width,
                continent.h * canvas.height
            );
        });
        
        // Add some land variation/texture
        const landVariations = ['#3d6b1f', '#1d4010', '#4d7b2f'];
        ctx.globalAlpha = 0.4;
        for (let i = 0; i < 300; i++) {
            ctx.fillStyle = landVariations[Math.floor(Math.random() * landVariations.length)];
            ctx.fillRect(
                Math.random() * canvas.width * 0.8,
                Math.random() * canvas.height * 0.8,
                Math.random() * 80 + 5,
                Math.random() * 80 + 5
            );
        }
        ctx.globalAlpha = 1;
        
        // Add some clouds (white wispy areas)
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        for (let i = 0; i < 40; i++) {
            ctx.beginPath();
            ctx.arc(
                Math.random() * canvas.width,
                Math.random() * canvas.height,
                Math.random() * 80 + 20,
                0,
                Math.PI * 2
            );
            ctx.fill();
        }

        const texture = new THREE.CanvasTexture(canvas);
        const material = new THREE.MeshPhongMaterial({
            map: texture,
            emissive: 0x1a3a52,
            shininess: 8
        });

        this.globe = new THREE.Mesh(geometry, material);
        this.scene.add(this.globe);

        // Atmosphere glow
        const atmosphereGeometry = new THREE.SphereGeometry(1.02, 128, 128);
        const atmosphereMaterial = new THREE.MeshPhongMaterial({
            color: 0x87ceeb,
            emissive: 0x4da6ff,
            wireframe: false,
            transparent: true,
            opacity: 0.15
        });
        const atmosphere = new THREE.Mesh(atmosphereGeometry, atmosphereMaterial);
        this.scene.add(atmosphere);

        // Grid lines (subtle latitude/longitude)
        const gridGeometry = new THREE.BufferGeometry();
        const gridPoints = [];
        
        // Latitude lines
        for (let lat = -60; lat <= 60; lat += 30) {
            const latRad = (lat * Math.PI) / 180;
            for (let lon = -180; lon <= 180; lon += 2) {
                const lonRad = (lon * Math.PI) / 180;
                const x = Math.cos(latRad) * Math.cos(lonRad);
                const y = Math.sin(latRad);
                const z = Math.cos(latRad) * Math.sin(lonRad);
                gridPoints.push(x, y, z);
            }
        }

        gridGeometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(gridPoints), 3));
        const gridMaterial = new THREE.LineBasicMaterial({ color: 0x004080, transparent: true, opacity: 0.1 });
        this.gridLines = new THREE.LineSegments(gridGeometry, gridMaterial);
        this.scene.add(this.gridLines);
    }

    createLighting() {
        // Sun light
        const sunLight = new THREE.DirectionalLight(0xffffff, 1.2);
        sunLight.position.set(5, 3, 5);
        this.scene.add(sunLight);

        // Ambient light for overall illumination
        const ambientLight = new THREE.AmbientLight(0x4080ff, 0.6);
        this.scene.add(ambientLight);
    }

    addEarthquakeMarker(latitude, longitude, magnitude) {
        // Convert lat/lon to 3D coordinates on sphere
        const latRad = (latitude * Math.PI) / 180;
        const lonRad = (longitude * Math.PI) / 180;
        
        const x = Math.cos(latRad) * Math.cos(lonRad);
        const y = Math.sin(latRad);
        const z = Math.cos(latRad) * Math.sin(lonRad);

        // Scale based on magnitude (5=1, 8=4)
        const scale = Math.max(0.02, (magnitude - 4) * 0.15);

        // Create marker (small sphere)
        const markerGeometry = new THREE.SphereGeometry(scale, 32, 32);
        
        // Color based on magnitude
        let color = 0x00ff00; // Green for low
        if (magnitude >= 5) color = 0xffff00; // Yellow
        if (magnitude >= 6) color = 0xff8800; // Orange
        if (magnitude >= 7) color = 0xff0000; // Red

        const markerMaterial = new THREE.MeshPhongMaterial({ 
            color: color,
            emissive: color,
            emissiveIntensity: 0.8,
            wireframe: false
        });
        const marker = new THREE.Mesh(markerGeometry, markerMaterial);

        // Position on surface
        const surfaceOffset = 1.01;
        marker.position.set(x * surfaceOffset, y * surfaceOffset, z * surfaceOffset);

        // Store data for interaction
        marker.userData = {
            type: 'earthquake',
            latitude,
            longitude,
            magnitude
        };

        this.scene.add(marker);

        // Create pulse animation
        this.animateMarkerPulse(marker);
    }

    animateMarkerPulse(marker) {
        const originalScale = marker.scale.x;
        const animate = () => {
            const time = Date.now() * 0.001;
            const pulse = Math.sin(time * 2) * 0.3 + 0.7;
            marker.scale.set(pulse, pulse, pulse);
            requestAnimationFrame(animate);
        };
        animate();
    }

    startAnimation() {
        const animate = () => {
            requestAnimationFrame(animate);

            // Rotate globe slowly
            this.globe.rotation.y += 0.0001;

            this.renderer.render(this.scene, this.camera);
        };
        animate();
    }

    setupMouseControls() {
        this.renderer.domElement.addEventListener('mousemove', (event) => {
            this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

            this.raycaster.setFromCamera(this.mouse, this.camera);
            const intersects = this.raycaster.intersectObjects(this.scene.children);

            if (intersects.length > 0) {
                const obj = intersects[0].object;
                if (obj.userData.type === 'earthquake') {
                    this.renderer.domElement.style.cursor = 'pointer';
                    // Could show tooltip here
                }
            } else {
                this.renderer.domElement.style.cursor = 'default';
            }
        });

        this.renderer.domElement.addEventListener('click', (event) => {
            this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

            this.raycaster.setFromCamera(this.mouse, this.camera);
            const intersects = this.raycaster.intersectObjects(this.scene.children);

            if (intersects.length > 0) {
                const obj = intersects[0].object;
                if (obj.userData.type === 'earthquake') {
                    this.onEarthquakeClick(obj.userData);
                }
            }
        });

        // Zoom controls
        this.renderer.domElement.addEventListener('wheel', (event) => {
            event.preventDefault();
            this.camera.position.z += event.deltaY * 0.001;
            this.camera.position.z = Math.max(1.5, Math.min(5, this.camera.position.z));
        });
    }

    onEarthquakeClick(data) {
        const message = `Magnitude ${data.magnitude.toFixed(1)} at ${data.latitude.toFixed(2)}°N, ${data.longitude.toFixed(2)}°E`;
        console.log('Clicked earthquake:', message);
        
        // Dispatch event for UI update
        window.dispatchEvent(new CustomEvent('earthquakeSelected', { detail: data }));
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    clear() {
        // Remove all earthquake markers
        if (!this.scene || !this.scene.children) return;
        
        const childrenToRemove = [];
        this.scene.children.forEach(obj => {
            if (obj.userData && obj.userData.type === 'earthquake') {
                childrenToRemove.push(obj);
            }
        });
        
        childrenToRemove.forEach(obj => {
            this.scene.remove(obj);
        });
    }
}

// Global instance
window.globe3d = null;

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    window.globe3d = new Globe3D();
});
