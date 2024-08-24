import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import store from '@store';

class ColorMaterial extends THREE.MeshStandardMaterial {
	constructor(p, color) {
		super();
		this.isColorMaterial = true;
		this.type = 'ColorMaterial';
		this.setValues(p);
		this.color = new THREE.Color(0x000000);
		this.emissive = new THREE.Color(color);
		this.emissiveIntensity = 2;
	}

	copy(source) {
		super.copy(source);
		return (this);
	}
}

const FOV = 75;
const ZNEAR = 0.1;
const ZFAR = 1000;

const assets = {
	ball: {
		texture: '/ressources/texture/cyberSphere.png',
		radius: 1
	},
	paddle: {
		texture: '/ressources/texture/cyberPaddle.png',
		width: 1.6,
		height: 1,
		depth: 7
	},
	map: {
		model: store.getters.selectedMapPath,
		scale: 20
	},
	lights: {
		ambient: {
			color: 0xf0f0f0
		},
		directional: {
			color: 0xffffff,
			intensity: 1,
			/** Direction has to be normalized !!! */
			direction: {
				x: 5,
				y: 10,
				z: 5
			}
		}
	},
	camera: {
		position: {
			x: 60,
			y: 5,
			z: 0
		},
		lookat: {
			x: 0,
			y: -20,
			z: 0
		}
	}
};

export default class PongRenderer {
	#canvas;
	#canvas_container;

	#renderer;
	#render_pass;
	#bloom_pass;
	#composer;

	#camera;
	#scene;

	#textures = {
		ball: undefined,
		paddle: undefined
	};

	#materials = {
		neon: undefined
	};

	#objects = {
		lights: {
			ambient: undefined,
			directional: undefined
		},
		ball: undefined,
		paddle_1: undefined,
		paddle_2: undefined,
		map: undefined
	};

	constructor(
		canvas,
		canvas_container,
		theme_color
	) {
		const create_composer = () => {
			const renderer_config = {
				antialias: true,
				canvas: canvas.value
			};
			
			this.#canvas = canvas;
			this.#canvas_container = canvas_container;
			this.#renderer = new THREE.WebGLRenderer(renderer_config);
			const setup_resize = () => {
				window.addEventListener('resize', this.onWindowResize, false);
			}
			this.#renderer.setSize(this.#canvas_container.value.clientWidth, this.#canvas_container.value.clientHeight, true);
			setup_resize();
			this.#composer = new EffectComposer(this.#renderer);
			this.#render_pass = new RenderPass(this.#scene, this.#camera);
			this.#bloom_pass = new UnrealBloomPass(
				// HACK: Will be fixed when the game canvas becomes responsive
				new THREE.Vector2(this.#canvas_container.value.clientWidth, this.#canvas_container.value.clientHeight),
				0.2,  // strength
				0.2,  // radius
				0.1   // threshold
			);
			this.#composer.addPass(this.#render_pass);
			this.#composer.addPass(this.#bloom_pass);
		};

		const load_textures = () => {
			const loader = new THREE.TextureLoader();
			const filter = (t) => t.minFilter = THREE.LinearFilter;

			this.#textures.ball = loader.load(assets.ball.texture, filter);
			this.#textures.paddle = loader.load(assets.paddle.texture, filter);
		};

		const load_materials = () => {
			this.#materials.neon = new THREE.MeshStandardMaterial({
				color: new THREE.Color(theme_color),
				emissive: new THREE.Color(theme_color),
				emissiveIntensity: 2,
				metalness: 2,
				roughness: 0.1
			});
		};

		const load_objects = () => {
			const load_ball = () => {
				const SIZE = 30;

				this.#objects.ball = new THREE.Mesh(
					new THREE.SphereGeometry(assets.ball.radius, SIZE, SIZE),
					this.#materials.neon
				);
			};

			const load_paddles = () => {
				const paddle_geometry = new THREE.BoxGeometry(
					assets.paddle.width,
					assets.paddle.height,
					assets.paddle.depth,
				);

				this.#objects.paddle_1 = new THREE.Mesh(
					paddle_geometry,
					this.#materials.neon
				);
				this.#objects.paddle_2 = new THREE.Mesh(
					paddle_geometry,
					this.#materials.neon
				);
			};

			const load_map = () => {
				const apply_color_material = (o) => {
					if (o.isMesh)
						o.material = new ColorMaterial(o.material, theme_color)
				};

				const on_loaded = (model) => {
					const SCALE = assets.map.scale;

					this.#objects.map = model.scene;
					this.#objects.map.traverse(apply_color_material);
					this.#objects.map.scale.set(SCALE, SCALE, SCALE);
					this.#scene.add(this.#objects.map);
				};

				const map = new GLTFLoader();

				map.setDRACOLoader(new DRACOLoader());
				map.load(assets.map.model, on_loaded, undefined, undefined);
			};

			load_map();
			load_ball();
			load_paddles();
		};

		const load_lights = () => {
			this.#objects.lights.ambient = new THREE.AmbientLight(
				assets.lights.ambient.color
			);
			this.#objects.lights.directional = new THREE.DirectionalLight(
				assets.lights.directional.color,
				assets.lights.directional.intensity
			);
		}

		const setup = () => {
			const setup_lights = () => {
				this.#objects.lights.directional.position.set(
					assets.lights.directional.direction.x,
					assets.lights.directional.direction.y,
					assets.lights.directional.direction.z
				);
				this.#objects.lights.directional.position.normalize();
				this.#scene.add(this.#objects.lights.ambient);
				this.#scene.add(this.#objects.lights.directional);
			};

			const setup_ball = () => {
				this.#scene.add(this.#objects.ball);
			};

			const setup_paddles = () => {
				this.#scene.add(this.#objects.paddle_1);
				this.#scene.add(this.#objects.paddle_2);
			};

			const setup_camera = () => {
				this.#camera.position.set(
					assets.camera.position.x,
					assets.camera.position.y,
					assets.camera.position.z
				);
				this.#camera.lookAt(new THREE.Vector3(
					assets.camera.lookat.x,
					assets.camera.lookat.y,
					assets.camera.lookat.z
				));
			};

			setup_lights();
			setup_ball();
			setup_paddles();
			setup_camera();
		};

		this.#camera = new THREE.PerspectiveCamera(FOV, 16 / 9, ZNEAR, ZFAR);
		this.#scene = new THREE.Scene();
		create_composer();
		load_textures();
		load_materials();
		load_objects();
		load_lights();
		setup();
	}

	updateState = (
		ball={
			position: {x: 0, y: 0}
		},
		paddle1={
			position: {x: 0, y: 0}
		},
		paddle2={
			position: {x: 0, y: 0}
		}
	) => {
		const update_ball = () => {
			const { x, y } = ball.position;

			this.#objects.ball.position.set(x, -19, y);
		};

		const update_paddle_1 = () => {
			const { x, y } = paddle1.position;
			
			this.#objects.paddle_1.position.set(x, -19, y);
		};
		
		const update_paddle_2 = () => {
			const { x, y } = paddle2.position;

			this.#objects.paddle_2.position.set(x, -19, y);
		};

		update_ball();
		update_paddle_1();
		update_paddle_2();
	}

	onWindowResize = () => {
		console.log("canvas container client : ", this.#canvas_container.value.clientWidth + "x" + this.#canvas_container.value.clientHeight);
		this.#renderer.setSize(this.#canvas_container.value.clientWidth, this.#canvas_container.value.clientHeight, true);
		this.#composer.setSize(this.#canvas_container.value.clientWidth, this.#canvas_container.value.clientHeight);
		this.#render_pass.setSize(this.#canvas_container.value.clientWidth, this.#canvas_container.value.clientHeight);
		this.#bloom_pass.setSize(this.#canvas_container.value.clientWidth, this.#canvas_container.value.clientHeight);
	};

	render() {
		this.#composer.render();
	}

	cleanup = () => {
		window.removeEventListener('resize', this.onWindowResize);
		if (this.#objects.ball.geometry)
			this.#objects.ball.geometry.dispose();
		if (this.#objects.paddle_1.geometry)
			this.#objects.paddle_1.geometry.dispose();
		if (this.#objects.paddle_2.geometry)
			this.#objects.paddle_2.geometry.dispose();
		if (this.#objects.map.geometry)
			this.#objects.map.geometry.dispose();
		this.#objects.map.traverse((e) => {
			if (!e.isMesh)
				return ;
			e.geometry.dispose();
			e.material.dispose();
		})
		if (this.#materials.neon)
			this.#materials.neon.dispose();
		if (this.#textures.ball)
			this.#textures.ball.dispose();
		if (this.#textures.paddle)
			this.#textures.paddle.dispose();
		if (this.#composer)
			this.#composer.dispose();
		if (this.#render_pass)
			this.#render_pass.dispose();
		if (this.#bloom_pass)
			this.#bloom_pass.dispose();
		if (this.#renderer)
			this.#renderer.dispose();
	}
}
