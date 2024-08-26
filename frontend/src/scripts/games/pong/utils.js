export const Direction = Object.freeze({
	RIGHT: 1,
	LEFT: -1,
	NONE: 0
});

export const Side = Object.freeze({
	ONE: 0,
	TWO: 1
});

export const integer_as_direction = (integer) => {
	if (integer > 0)
		return (Direction.RIGHT);
	if (integer < 0)
		return (Direction.LEFT);
	return (Direction.NONE);
}
