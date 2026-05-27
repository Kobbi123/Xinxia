ctx.setTransform(dpr,0,0,dpr,0,0);
}
window.addEventListener('resize', resize);
resize();

let running = false;
const particles = [];
const rings = [];
const spirits = []; // xianxia spirit particles
const colors = ['#ffb3b3','#ffd699','#fff99a','#b6ffb6','#aaffff','#a9c9ff','#d2a3ff','#ffd2f0'];

function rand(min,max){ return Math.random()*(max-min)+min; }

/* Basic particle classes */
class Particle {
  constructor(x,y,color,speed,angle,life,size){
	this.x = x; this.y = y;
	this.vx = Math.cos(angle)*speed;
	this.vy = Math.sin(angle)*speed;
	this.color = color;
	this.life = life; this.age = 0;
	this.size = size;
	this.gravity = 0.06;
	this.friction = 0.995;
  }
  update(dt){
	this.age += dt;
	this.vy += this.gravity * dt * 60;
	this.vx *= this.friction;
	this.vy *= this.friction;
	this.x += this.vx * dt * 60;
	this.y += this.vy * dt * 60;
  }
  draw(ctx){
	const t = 1 - (this.age / this.life);
	if (t <= 0) return;
	ctx.globalCompositeOperation = 'lighter';
	ctx.fillStyle = this.color;
	ctx.beginPath();
	ctx.arc(this.x, this.y, this.size * t, 0, Math.PI*2);
	ctx.fill();
  }
}

class Spark extends Particle {
  constructor(x,y,color,speed,angle,life,size){
	super(x,y,color,speed,angle,life,size);
	this.size = size || rand(1.2,3.8);
  }
}

/* Ring effect on explosion */
class Ring {
  constructor(x,y,color){ this.x=x; this.y=y; this.r=0; this.alpha=0.95; this.color=color; }
  update(dt){ this.r += 120 * dt; this.alpha -= 0.9 * dt; }
  draw(ctx){
	if (this.alpha <= 0) return;
	ctx.globalCompositeOperation = 'lighter';
	ctx.strokeStyle = this.color;
	ctx.lineWidth = 2;
	ctx.globalAlpha = Math.max(0, this.alpha);
	ctx.beginPath();
	ctx.arc(this.x, this.y, this.r, 0, Math.PI*2);
	ctx.stroke();
	ctx.globalAlpha = 1;
  }
}

/* Spirit: long, soft, curved particle for xianxia feel */
class Spirit {
  constructor(x,y, hue){
	this.x = x; this.y = y;
	this.age = 0;
	this.life = rand(2.8,5.5); // long-lived
	this.baseSize = rand(8,16);
	this.hue = hue;
	this.vx = rand(-0.6,0.6);
	this.vy = rand(-0.2,-1.2);
	this.wobble = rand(0.8,2.2);

