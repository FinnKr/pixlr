<script>
	// https://svelte.dev/repl/c4fbeea94855451ebed2f86d4b61572e?version=3.38.2
	// v1.2 - added keyboard nav for colors
	// @todo still a bug when the dropdown opens, we should focus on the already selected color, this only works when you click it open, close it and open again

	import { v4 as uuid } from "uuid";
	import { clickOutside } from "../scripts/clickOutside.ts";
	import { tick } from "svelte";

	// Initial value
	export let id = uuid();
	export let value = "#000000";

	// Our color set
	let values = [
		[
			"#000000",
			"#990000",
			"#bf9000",
			"#38761d",
			"#0b5394",
			"#351c75",
			"#741b47",
		],
		[
			"#323232",
			"#cc0000",
			"#f1c232",
			"#6aa84f",
			"#3d85c6",
			"#674ea7",
			"#a64d79",
		],
		[
			"#4c4c4c",
			"#e06666",
			"#ffd966",
			"#93c47d",
			"#6fa8dc",
			"#8e7cc3",
			"#c27ba0",
		],
		[
			"#ffffff",
			"#ea9999",
			"#ffe599",
			"#b6d7a8",
			"#9fc5e8",
			"#b4a7d6",
			"#d5a6bd",
		],
	];

	// Keyboard shortcut
	let trigger = "Escape";
	function handleKeydown(e) {
		if (e.key == trigger) {
			ddActive = false;
		}
	}

	let windowHeight;
	let top;

	let ddActive = false;

	let ddHeight = 158;
	// ddHeight is initially undefined so we can't get the correct values from binding; that's why we have a default
	// todo render offscreen for .1sec to get the height automatically?

	let inputHeight;

	async function toggleDropdown(e) {
		if (
			e.clientY + inputHeight < ddHeight ||
			windowHeight - ddHeight - inputHeight - e.clientY > 0
		) {
			top = false;
		} else {
			top = true;
		}

		ddActive = !ddActive;

		await tick();
		if (ddActive) {
			//document.querySelector('.color-block.active').focus();
		}
	}

	function clickOutsideDropdown() {
		ddActive = false;
	}

	function changeValue(innerValue) {
		value = innerValue;
		ddActive = false;
	}

	function keyboardGridNav(e, index) {
		const focussedElement = document.activeElement.id;

		let myRow = parseInt(
			focussedElement.charAt(focussedElement.length - 3)
		);
		let myIndex = parseInt(
			focussedElement.charAt(focussedElement.length - 1)
		);
		let nextRow;
		let prevRow;
		let nextIndex;
		let prevIndex;

		switch (e.keyCode) {
			// left arrow
			case 37:
				prevIndex = myIndex - 1;
				if (prevIndex > -1) {
					document
						.getElementById(id + "-" + myRow + "-" + prevIndex)
						.focus();
				}
				break;
			// top arrow
			case 38:
				prevRow = myRow - 1;
				if (prevRow > -1) {
					document
						.getElementById(id + "-" + prevRow + "-" + myIndex)
						.focus();
				}
				break;
			// right arrow
			case 39:
				nextIndex = myIndex + 1;
				if (nextIndex < values[0].length) {
					document
						.getElementById(id + "-" + myRow + "-" + nextIndex)
						.focus();
				}
				break;
			// down arrow
			case 40:
				nextRow = myRow + 1;
				if (nextRow < values.length) {
					document
						.getElementById(id + "-" + nextRow + "-" + myIndex)
						.focus();
				}
				break;
		}
	}
</script>

<svelte:window bind:innerHeight={windowHeight} on:keydown={handleKeydown} />

<div class="color-picker-holder">
	<div class="color-picker-inner">
		<button
			bind:clientHeight={inputHeight}
			class="select-color"
			on:click={(e) => toggleDropdown(e)}
			class:fake-focus={ddActive}
		>
			<div style="display: flex;">
				<div style="background: {value};" class="color-block" />
				<div class="caret" class:top style="margin-right: .2rem;" />
			</div>
		</button>
		<input type="text" bind:value />
	</div>

	{#if ddActive}
		<div
			class:top
			bind:clientHeight={ddHeight}
			class="values-dropdown"
			use:clickOutside
			on:click_outside={clickOutsideDropdown}
		>
			<div class="values-dropdown-grid">
				{#each values as val, index}
					{#each val as innerValue, innerIndex}
						<button
							id="{id}-{index}-{innerIndex}"
							class:active={innerValue == value}
							on:keydown={(e) => keyboardGridNav(e, innerIndex)}
							style="background: {innerValue};"
							on:click={() => {
								changeValue(innerValue);
							}}
							class="color-block"
						/>
					{/each}
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	.color-picker-holder {
		position: relative;
	}

	.color-picker-inner {
		display: flex;
		height: 35px;
	}

	.select-color {
		border: 1px solid #ccc;
		padding: 3px;
		border-radius: 0.2rem;
		margin-right: 0.4rem;
		background: #fff;
		height: 35px;
	}

	.caret {
		width: 0;
		height: 0;
		border-left: 4px solid transparent;
		border-right: 4px solid transparent;
		border-top: 4px solid #555;
		position: relative;
		top: 10px;
		margin-left: 4px;
	}

	.caret.top {
		border-left: 4px solid transparent;
		border-right: 4px solid transparent;
		border-bottom: 4px solid #555;
		border-top: none;
	}

	.active {
		box-shadow: inset 0 0 0 1px #fff, 0 0 3px 1px rgba(0, 0, 0, 0.25);
	}

	.fake-focus,
	input:focus,
	button:focus {
		outline: 0;
		box-shadow: 0 0 0 2px #18a0fb;
		border-color: #18a0fb;
	}

	input {
		border: 1px solid #ccc;
		height: 35px;
		border-radius: 0.2rem;
	}

	.color-block {
		border-radius: 0.2rem;
		width: 24px;
		height: 24px;
		line-height: 0;
		font-size: 0;
	}

	.values-dropdown {
		padding: 1rem;
		position: absolute;
		z-index: 1;
		top: 40px;
		background: white;
		border: 1px solid #ccc;
		border-radius: 0.3rem;
	}

	.values-dropdown-grid {
		grid-template-columns: repeat(7, 24px);
		grid-template-rows: 24px 24px;
		grid-gap: 10px;
		display: grid;
	}

	.values-dropdown.top {
		top: auto;
		bottom: 40px;
	}

	.values-dropdown button {
		border: none;
	}
</style>
