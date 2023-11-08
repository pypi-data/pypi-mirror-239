<script lang="ts">
	export let value: string;
	export let samples_dir: string;
	export let type: "gallery" | "table";
	export let selected = false;
</script>

<div
	class:table={type === "table"}
	class:gallery={type === "gallery"}
	class:selected
	style="justify-content: center; align-items: center; display: flex; flex-direction: column;"
>
	<iframe title="Example pdf" src={samples_dir + value} />
</div>

<style>
	.gallery {
		padding: var(--size-1) var(--size-2);
	}
</style>
