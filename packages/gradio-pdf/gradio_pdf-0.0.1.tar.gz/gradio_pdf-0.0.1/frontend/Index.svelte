  <script lang="ts">
	import {tick} from "svelte";
	import PdfUploadText from "./PdfUploadText.svelte";
	import type { Gradio } from "@gradio/utils";
	import { Block, BlockLabel } from "@gradio/atoms";
	import { File } from "@gradio/icons";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import type { FileData } from "@gradio/client";
	import { normalise_file } from "@gradio/client";
	import { Upload, ModifyUpload } from "@gradio/upload"; 

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: FileData | null = null;
	export let container = true;
	export let scale: number | null = null;
	export let root: string;
	export let height: number = 500;
	export let label: string;
	export let proxy_url: string;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let gradio: Gradio<{
		change: never;
		upload: never;
	}>;

	let _value = value;
	let old_value = _value;


	async function handle_clear() {
		_value = null;
		await tick();
		gradio.dispatch("change");
	}
	async function handle_upload({detail}: CustomEvent<FileData>): Promise<void> {
		value = detail;
		await tick();
		gradio.dispatch("change");
		gradio.dispatch("upload");
	}
      
	$: _value = normalise_file(value, root, proxy_url);

	$: if(JSON.stringify(old_value) != JSON.stringify(_value)) {
		old_value = _value;
		gradio.dispatch("change");
	}

</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
		/>
	{/if}
	<BlockLabel
		show_label={label !== null}
		Icon={File}
		float={value === null}
		label={label || "File"}
	/>
	{#if _value}
		<ModifyUpload i18n={gradio.i18n} on:clear={handle_clear} absolute />
		<iframe title={label} src={_value.url} width="100%" height={height} />
	{:else}
		<Upload
			on:load={handle_upload}
			filetype={"application/pdf"}
			file_count="single"
			{root}
		>
			<PdfUploadText/>
		</Upload>
	{/if}
</Block>
