"use client";

import React, { useEffect, useState } from "react";
import Image from "next/image";
import { DataModel } from "./model";

type FetchState = {
	items: DataModel[];
	loading: boolean;
	error?: string;
};

export default function Home() {
	const [state, setState] = useState<FetchState>({ items: [], loading: true });

	const testItems: DataModel[] = [
		{
			title: "Artikel 1",
			date: new Date(),
			author: "Author 1",
			url: new URL("http://localhost:3000"),
			source: "Source 1",
			thumbnail: new URL("http://example.com/thumb1.jpg"),
			tags: ["tag1", "tag2"],
			first_lines:
				"First lines of article 1, just some random stuff. Want this to be like about two sentences long or something. This should be enough.",
			content: "Full content of article 1",
		},
	];

	useEffect(() => {
		// let mounted = true;
		// const fetchArticles = async () => {
		// 	try {
		// 		const res = await fetch("/api/articles?limit=50");
		// 		if (!res.ok) throw new Error(`HTTP ${res.status}`);
		// 		const data: DataModel[] = await res.json();
		// 		if (!mounted) return;
		// 		setState({ items: data.slice(0, 50), loading: false });
		// 	} catch (err: any) {
		// 		if (!mounted) return;
		// 		setState({ items: [], loading: false, error: err?.message ?? "Failed to load" });
		// 	}
		// };

		// fetchArticles();
		// return () => {
		// 	mounted = false;
		// };

		setState({ items: testItems, loading: false });
	}, []);

	return (
		<div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
			<main className="flex min-h-screen w-full max-w-5xl flex-col items-center py-12 px-6 bg-white dark:bg-black">
				<header className="w-full mb-6">
					<h1 className="text-2xl font-semibold text-zinc-900 dark:text-zinc-100">
						Latest Articles
					</h1>
					<p className="text-sm text-zinc-600 dark:text-zinc-400">
						Up to 50 articles from various outlets
					</p>
				</header>

				{state.loading ? (
					<div className="w-full flex items-center justify-center py-20 text-zinc-500">
						Loading...
					</div>
				) : state.error ? (
					<div className="w-full text-red-500">Error: {state.error}</div>
				) : (
					<div className="w-full">
						<div className="h-[70vh] overflow-auto pr-2">
							<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
								{state.items.map((item) => {
									const dateStr = item.date ? new Date(item.date).toLocaleString() : "Unknown date";
									return (
										<article
											key={(item as any).id ?? item.title}
											className="flex flex-col bg-white dark:bg-zinc-900 rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden border border-zinc-100 dark:border-zinc-800"
										>
											<div className="relative w-full h-40 bg-zinc-100 dark:bg-zinc-800">
                        {item.thumbnail ? (
                          <Image
                            src={item.thumbnail.toString()}
                            alt={item.title ?? "thumbnail"}
                            fill
                            style={{ objectFit: "cover" }}
                            sizes="(max-width: 768px) 100vw, 33vw"
                            unoptimized
                          />
                        ) : (
                          <div className="w-full h-full flex items-center justify-center text-zinc-400">
                            No image
                          </div>
                        )}
											</div>

											<div className="p-4 flex-1 flex flex-col">
												<h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 line-clamp-2">
													{item.title ?? "Untitled"}
												</h2>
												<p className="mt-2 text-xs text-zinc-600 dark:text-zinc-300 line-clamp-3">
													{item.first_lines ?? item.content ?? ""}
												</p>

												<div className="mt-auto pt-3 flex items-center justify-between text-xs text-zinc-500 dark:text-zinc-400">
													<span>{item.source ?? "Unknown source"}</span>
													<time>{dateStr}</time>
												</div>
											</div>
										</article>
									);
								})}
							</div>
						</div>
					</div>
				)}
			</main>
		</div>
	);
}
