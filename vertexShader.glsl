attribute vec4 aPosition;
varying vec2 vPos;

void main() {
  gl_Position = aPosition;
  vPos = aPosition.xy;
}