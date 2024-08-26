import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import store from '@store';
import { DEFAULT_SCENE_STATE } from './model';

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
const ASPECT_RATIO = 16. / 9.;
const ZNEAR = 0.1;
const ZFAR = 1000;

export default class PongRenderer {
	#canvas_container;

	#renderer;
	#render_pass;
	#bloom_pass;
	#composer;

	#resizer;

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
		config,
		canvas,
		canvas_container,
		theme_color
	) {
		const create_composer = () => {
			const renderer_config = {
				antialias: true,
				canvas: canvas.value
			};
			
			const width = canvas_container.value.clientWidth;
			const height = canvas_container.value.clientHeight;

			this.#canvas_container = canvas_container;
			this.#renderer = new THREE.WebGLRenderer(renderer_config);
			this.#renderer.setSize(width, height, true);
			this.#composer = new EffectComposer(this.#renderer);
			this.#render_pass = new RenderPass(this.#scene, this.#camera);
			this.#bloom_pass = new UnrealBloomPass(
				new THREE.Vector2(width, height),
				0.4,  // strength
				0.5,  // radius
				0.4   // threshold
			);
			this.#composer.addPass(this.#render_pass);
			this.#composer.addPass(this.#bloom_pass);
			this.#resizer = window.addEventListener(
				'resize', this.#onWindowResize, false
			);
		};

		const load_textures = () => {
			const loader = new THREE.TextureLoader();
			const filter = (t) => t.minFilter = THREE.LinearFilter;

			this.#textures.ball = loader.load(config.ball.texture, filter);
			this.#textures.paddle = loader.load(config.paddle.texture, filter);
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
					new THREE.SphereGeometry(config.ball.radius, SIZE, SIZE),
					this.#materials.neon
				);
			};

			const load_paddles = () => {
				const paddle_geometry = new THREE.BoxGeometry(
					config.paddle.width,
					config.paddle.height,
					config.paddle.depth,
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
					const SCALE = config.map.scale;

					this.#objects.map = model.scene;
					this.#objects.map.traverse(apply_color_material);
					this.#objects.map.scale.set(SCALE, SCALE, SCALE);
					this.#objects.map.position.set(
						config.map.position.x,
						config.map.position.y,
						config.map.position.z
					);
					this.#scene.add(this.#objects.map);
				};

				const map = new GLTFLoader();
				const map_file = store.getters.selectedMapPath;

				map.setDRACOLoader(new DRACOLoader());
				map.load(map_file, on_loaded, undefined, undefined);
			};

			load_map();
			load_ball();
			load_paddles();
		};

		const load_lights = () => {
			this.#objects.lights.ambient = new THREE.AmbientLight(
				config.lights.ambient.color
			);
			this.#objects.lights.directional = new THREE.DirectionalLight(
				config.lights.directional.color,
				config.lights.directional.intensity
			);
		}

		const setup = () => {
			const setup_lights = () => {
				this.#objects.lights.directional.position.set(
					config.lights.directional.direction.x,
					config.lights.directional.direction.y,
					config.lights.directional.direction.z
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
					config.camera.position.x,
					config.camera.position.y,
					config.camera.position.z
				);
				this.#camera.lookAt(new THREE.Vector3(
					config.camera.lookat.x,
					config.camera.lookat.y,
					config.camera.lookat.z
				));
			};

			setup_lights();
			setup_ball();
			setup_paddles();
			setup_camera();
		};

		const aspect_ratio_dims = config.camera.aspect_ratio;

		this.#scene = new THREE.Scene();
		this.#camera = new THREE.PerspectiveCamera(
			config.camera.fov,
			aspect_ratio_dims.width / aspect_ratio_dims.height,
			config.camera.znear,
			config.camera.zfar
		);
		create_composer();
		load_textures();
		load_materials();
		load_objects();
		load_lights();
		setup();
	}

	updateState = (state=DEFAULT_SCENE_STATE) => {
		const set = (self, state) =>
			self.position.set(state.position.x, 0, state.position.y);

		set(this.#objects.ball, state.ball);
		set(this.#objects.paddle_1, state.paddles[0]);
		set(this.#objects.paddle_2, state.paddles[1]);
	}

	#onWindowResize = () => {
		const canvas_container = this.#canvas_container.value;
		const width = canvas_container.clientWidth;
		const height = canvas_container.clientHeight;

		this.#renderer.setSize(width, height, true);
		this.#composer.setSize(width, height);
		this.#render_pass.setSize(width, height);
		this.#bloom_pass.setSize(width, height);
	};

	render() {
		this.#composer.render();
	}

	cleanup = () => {
		window.removeEventListener('resize', this.#onWindowResize);
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
