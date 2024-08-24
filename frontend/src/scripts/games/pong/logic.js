import PongModel from './model';

export default class PongLogic {
	/** @type {PongModel} */
	#model;
	#callbacks;

	constructor(
		/** @type {PongModel} */ model,
		callbacks={
			onUpdateFinished: (
				ball={
					position: {x: 0, y: 0}
				},
				paddle1={
					position: {x: 0, y: 0}
				},
				paddle2={
					position: {x: 0, y: 0}
				}
			) => {},
			onPlayerOneInputRequested: () => Direction.NONE,
			onPlayerTwoInputRequested: () => Direction.NONE
		}
	) {
		this.#model = model;
		this.#callbacks = callbacks;
	}

	step = () => {
		this.#callbacks.onUpdateFinished(
			this.#model.getBall(),
			this.#model.getPaddle1(),
			this.#model.getPaddle2()
		);
	}

	setCallbackUpdateFinished = (onUpdateFinished) => {
		this.#callbacks.onUpdateFinished = onUpdateFinished;
	}
}
