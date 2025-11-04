// Interface for the decided data document model
export interface DataModel {
	title: string;
	date: Date;
	author: string;
	url: URL;
	source: string;
	thumbnail: URL;
	tags: string[];
	first_lines: string;
	content: string;
}
