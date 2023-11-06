(function() {
    // Add the particles div to the body
    var particlesDiv = document.createElement('div');
    particlesDiv.id = 'particles-js';
    document.body.insertBefore(particlesDiv, document.body.firstChild);

    // Add styles for particles div
    var css = '#particles-js { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; }',
        head = document.head || document.getElementsByTagName('head')[0],
        style = document.createElement('style');

    head.appendChild(style);

    style.type = 'text/css';
    if (style.styleSheet){
        // This is required for IE8 and below.
        style.styleSheet.cssText = css;
    } else {
        style.appendChild(document.createTextNode(css));
    }

    // Load particles.js library
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js';
    script.onload = function() {
        // Initialize particles.js after the library is loaded
        particlesJS("particles-js", {
            // ... the particles.js configuration goes here
            
            particles: {
                number: {
                    value: 40,
                    density: {
                        enable: true,
                        value_area: 800
                    }
                },
                color: {
                    // Adding multiple colors
                    value: ["#ffffff", "#ffdd59", "#f368e0", "#ff9f43", "#ee5253"]
                },
                shape: {
                    type: "circle",
                    stroke: {
                        width: 0,
                        color: "#000000"
                    },
                },
                opacity: {
                    value: 0.5,
                    random: false,
                    anim: {
                        enable: false,
                        speed: 2,
                        opacity_min: 0.1,
                        sync: false
                    }
                },
                size: {
                    // Making the particles smaller
                    value: 2.5,
                    random: true,
                    anim: {
                        enable: false,
                        speed: 40,
                        size_min: 0.1,
                        sync: false
                    }
                },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: "#ffffff",
                    opacity: 0.4,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 6,
                    direction: "none",
                    random: false,
                    straight: false,
                    out_mode: "out",
                    bounce: false,
                    attract: {
                        enable: false,
                        rotateX: 600,
                        rotateY: 1200
                    }
                }
            },
            interactivity: {
                // ... [interactivity settings]
            },
            retina_detect: true
        });
    };

    document.body.appendChild(script);
})();
