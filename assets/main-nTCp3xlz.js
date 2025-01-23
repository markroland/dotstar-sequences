(function(){const o=document.createElement("link").relList;if(o&&o.supports&&o.supports("modulepreload"))return;for(const r of document.querySelectorAll('link[rel="modulepreload"]'))t(r);new MutationObserver(r=>{for(const s of r)if(s.type==="childList")for(const a of s.addedNodes)a.tagName==="LINK"&&a.rel==="modulepreload"&&t(a)}).observe(document,{childList:!0,subtree:!0});function e(r){const s={};return r.integrity&&(s.integrity=r.integrity),r.referrerPolicy&&(s.referrerPolicy=r.referrerPolicy),r.crossOrigin==="use-credentials"?s.credentials="include":r.crossOrigin==="anonymous"?s.credentials="omit":s.credentials="same-origin",s}function t(r){if(r.ep)return;r.ep=!0;const s=e(r);fetch(r.href,s)}})();const C=800,B=800,S=.75,N=.03,W=S,g=.3,D="cuttlefish.png",H=1/30;let f,c,l;async function M(n){const o=new Image;o.src=n;try{await o.decode(),c=o.width,l=o.height;const t=new OffscreenCanvas(c,l).getContext("2d");t.drawImage(o,0,0),f=t.getImageData(0,0,c,l).data}catch(e){console.error("Error loading image:",e)}}async function G(n,o){try{const[e,t]=await Promise.all([fetch(n),fetch(o)]);if(!e.ok)throw new Error(`Vertex shader HTTP error ${e.status}`);if(!t.ok)throw new Error(`Fragment shader HTTP error ${t.status}`);const r=await e.text(),s=await t.text();return{vertexShaderSource:r,fragmentShaderSource:s}}catch(e){return console.error("Error loading shaders:",e),null}}function E(n,o,e){const t=n.createShader(o);if(n.shaderSource(t,e),n.compileShader(t),!n.getShaderParameter(t,n.COMPILE_STATUS)){const r=o===n.VERTEX_SHADER?"vertex":"fragment";return console.error(`${r} shader compilation error:`,n.getShaderInfoLog(t)),n.deleteShader(t),null}return t}async function V(){const n=document.getElementById("canvas");n.width=C,n.height=B,await M(D),console.log("Imaged Loaded. Width: "+c+", Height: "+l);const o=c,e=n.getContext("webgl");if(e)e.getParameter(e.VERSION).startsWith("WebGL 2")?console.log("WebGL 2.0 is supported"):console.log("WebGL 1.0 is supported (version "+e.VERSION+")");else{console.error("Unable to initialize WebGL. Your browser or machine may not support it.");return}const t=await G("vertexShader.glsl","fragmentShader.glsl");if(!t){console.error("Error loading shaders");return}const r=E(e,e.VERTEX_SHADER,t.vertexShaderSource),s=E(e,e.FRAGMENT_SHADER,t.fragmentShaderSource),a=e.createProgram();if(e.attachShader(a,r),e.attachShader(a,s),e.linkProgram(a),!e.getProgramParameter(a,e.LINK_STATUS))return console.error("Unable to link the shader program: "+e.getProgramInfoLog(a)),null;e.useProgram(a);const P=e.getUniformLocation(a,"u_frame"),y=e.getUniformLocation(a,"u_circleCount"),w=e.getUniformLocation(a,"u_circleRadius"),A=e.getUniformLocation(a,"u_circlePositions"),v=e.getUniformLocation(a,"u_circleColors"),U=e.getUniformLocation(a,"u_maskRadius"),_=e.createBuffer();e.bindBuffer(e.ARRAY_BUFFER,_);const T=new Float32Array([-1,-1,1,-1,-1,1,1,1]);e.bufferData(e.ARRAY_BUFFER,T,e.STATIC_DRAW);const p=e.getAttribLocation(a,"aPosition");e.enableVertexAttribArray(p),e.vertexAttribPointer(p,2,e.FLOAT,!1,0,0);function L(){const u=[],R=[];let m=0;const h=d*c*4;for(let i=0;i<o;i++){m=Math.PI*2*(i/o);const b=Math.cos(m)*S,I=Math.sin(m)*S;u.push(b,I);const x=g*f[h+i*4]/255,O=g*f[h+i*4+1]/255,F=g*f[h+i*4+2]/255;R.push(x,O,F)}e.uniform1i(P,d),e.uniform1i(y,o),e.uniform1f(w,N),e.uniform2fv(A,u),e.uniform3fv(v,R),e.uniform1f(U,W),e.clearColor(0,0,0,1),e.clear(e.COLOR_BUFFER_BIT),e.drawArrays(e.TRIANGLE_STRIP,0,4),d=(d+1)%l,setTimeout(L,H*1e3)}let d=0;L()}V();
