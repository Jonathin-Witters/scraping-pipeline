"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { DataModel } from "./model";
import {
	collection,
	getDocs,
	query,
	limit,
	getFirestore,
	orderBy,
	startAfter,
} from "firebase/firestore";
import { initializeApp } from "firebase/app";
import Link from "next/link";

type FetchState = {
	items: DataModel[];
	loading: boolean;
	error?: string;
};

export default function Home() {
	const sources = "VRT NWS, De Standaard, De Morgen, Nieuwsblad, HBVL, Telegraaf, GVA, De Volkskrant"; // Add used sources here
	const collections = ["vrtnws", "demorgen", "destandaard", "nieuwsblad", "hbvl", "telegraaf", "gva", "devolkskrant"]; // Firestore collection names

	const page_size = 100; // Number of articles to fetch at a time

	const [state, setState] = useState<FetchState>({ items: [], loading: true });

	// const [lastDoc, setLastDoc] = useState<any>(null); // previously used for single collection
	const [lastDocTime, setLastDocTime] = useState<Date | null>(null); // for multi-collection pagination

	// Optional heuristic to support balanced fetching, especially when considering loads of sources
	// possible con: may not show the absolute most recent page_size articles
	// but pro #1: ensures more variety in displayed sources (which is considered a goal of a news aggregator)
	// and pro #2: reduces the amount of data transferred from the backend when many sources are used, improving scalability
	// the math.ceil part ensures enough articles are fetched when few sources are used
	// the + page_size / 10 adds a small buffer to, even with many sources, allow multiple recent articles from the same source to be shown, 
	// avoiding stale sources to stay presented
	const adjusted_page_size = Math.ceil(page_size / collections.length) + page_size / 10;

	const [loadingMore, setLoadingMore] = useState(false); // for "Load More" button

	// used for UI testing
	const testItems: DataModel[] = [
		{
			title: "Artikel 1",
			date: new Date("2024-06-01T10:00:00Z"),
			author: "Author 1",
			url: new URL("http://localhost:3000"),
			source: "Source 1",
			thumbnail: new URL("http://example.com/thumb1.jpg"),
			tags: ["tag1", "tag2"],
			first_lines:
				"First lines of article 1, just some random stuff. Want this to be like about two sentences long or something. This should be enough.",
			content: ["Full content of article 1"],
		},
		{
			title: "Artikel 2",
			date: new Date("2024-04-02T11:00:00Z"),
			author: "Author 2",
			url: new URL("http://localhost:3000"),
			source: "Source 2",
			thumbnail: new URL("http://example.com/thumb2.jpg"),
			tags: ["tag1", "tag2"],
			first_lines:
				"First lines of article 2, just some random stuff. Want this to be like about two sentences long or something. This should be enough.",
			content: ["Full content of article 2"],
		},
		{
			title: "Artikel 3",
			date: new Date("2024-08-03T12:00:00Z"),
			author: "Author 3",
			url: new URL("http://localhost:3000"),
			source: "Source 3",
			thumbnail: new URL("http://example.com/thumb3.jpg"),
			tags: ["tag1", "tag2"],
			first_lines:
				"First lines of article 3, just some random stuff. Want this to be like about two sentences long or something. This should be enough.",
			content: ["Full content of article 3"],
		},
		// Extend for testing overflows, scrolling, ...
	];

	// Firebase configuration
	const firebaseConfig = {
		apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
		authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
		projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
		storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
		messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
		appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
		measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID,
	};

	const app = initializeApp(firebaseConfig);
	const db = getFirestore(app);

	const fetchArticles = async () => {
		try {
			// Query to fetch only most recent articles, and setting up for pagination

			// Previously used single collection
			// const q = lastDoc
			// 	? query(
			// 			collection(db, "articles"),
			// 			orderBy("date", "desc"),
			// 			startAfter(lastDoc),
			// 			limit(page_size)
			// 	  )
			// 	: query(collection(db, "articles"), orderBy("date", "desc"), limit(page_size));
			// const querySnapshot = await getDocs(q);
			//
			// // Keep track of last seen document for pagination
			// const lastVisible = querySnapshot.docs[querySnapshot.docs.length - 1];
			// setLastDoc(lastVisible);
			//
			// // Map documents to DataModel
			// const data: DataModel[] = querySnapshot.docs.map((doc) => ({
			// 	...(doc.data() as DataModel),
			// }));
			// setState((prev) => ({
			// 	...prev,
			// 	items: [...prev.items, ...data],
			// 	loading: false,
			// }));

			const queries = collections.map((collectionName) =>
				lastDocTime
					? query(
							collection(db, collectionName),
							orderBy("date", "desc"),
							startAfter(lastDocTime),
							limit(adjusted_page_size)
					  )
					: query(collection(db, collectionName), orderBy("date", "desc"), limit(adjusted_page_size))
			);

			// Fetch data from all collections
			const querySnapshots = await Promise.all(queries.map((q) => getDocs(q)));

			// Combine all documents into one array
			const allDocs = querySnapshots.flatMap((snapshot) =>
				snapshot.docs.map((doc) => ({ ...(doc.data() as DataModel), id: doc.id }))
			);

			// Sort combined documents by date (most recent first) and take the top `page_size`
			const sortedDocs = allDocs
				.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
				.slice(0, page_size);

			// Update lastDocTime to the last document's date in the sorted list
			setLastDocTime(sortedDocs[sortedDocs.length - 1]?.date);

			setState((prev) => ({
				...prev,
				items: [...prev.items, ...sortedDocs],
				loading: false,
			}));
		} catch (err: any) {
			setState({ items: [], loading: false, error: err?.message ?? "Failed to load" });
		}
	};

	const loadMore = async () => {
		setLoadingMore(true);
		await fetchArticles();
		setLoadingMore(false);
	};

	// Triggers initial fetch on page load
	useEffect(() => {
		fetchArticles();

		// Used for UI testing
		// setState({
		// 	items: testItems.sort((a, b) => b.date.getTime() - a.date.getTime()), // Sort by recency
		// 	loading: false,
		// });
	}, []);

	return (
		<div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
			<main className="flex min-h-screen w-full max-w-[80vw] flex-col items-center py-12 px-6 bg-white dark:bg-black">
				<header className="w-full mb-6">
					<h1 className="text-2xl font-semibold text-zinc-900 dark:text-zinc-100">
						Latest Articles
					</h1>
					<p className="text-sm text-zinc-600 dark:text-zinc-400">Scraped from: {sources}</p>
				</header>

				{state.loading ? (
					<div className="w-full flex items-center justify-center py-20 text-zinc-500">
						Loading...
					</div>
				) : state.error ? (
					<div className="w-full text-red-500">Error: {state.error}</div>
				) : (
					<div className="w-full">
						<div className="overflow-auto pr-2">
							<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
								{state.items.map((item) => {
									const dateStr = item.date
										? new Date(item.date).toLocaleString() + " (UTC)"
										: "Unknown date";
									return (
										<article
											key={item.title + item.source} // Should (realistically) guarantee uniqueness
											className="flex flex-col bg-white dark:bg-zinc-900 rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden border border-zinc-100 dark:border-zinc-800"
										>
											<Link href={item.url ?? "#"} target="_blank">
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
														{item.title}
													</h2>
													<p className="mt-2 text-xs text-zinc-600 dark:text-zinc-300 line-clamp-3">
														{item.first_lines ?? item.content[0] ?? ""}
													</p>

													<div className="mt-auto pt-3 flex items-center justify-between text-xs text-zinc-500 dark:text-zinc-400">
														<span>{item.source}</span>
														<time>{dateStr}</time>
													</div>
												</div>
											</Link>
										</article>
									);
								})}
							</div>
						</div>
					</div>
				)}
				{!state.loading && state.items.length > 0 && (
					<div className="w-full flex justify-center my-6">
						<button
							onClick={loadMore}
							disabled={loadingMore || !lastDocTime} // !lastDoc if using single collection
							className="px-4 py-2 rounded bg-zinc-900 text-white dark:bg-zinc-200 dark:text-black disabled:opacity-50 hover:cursor-pointer disabled:hover:cursor-not-allowed"
						>
							{
								loadingMore ? "Loading..." : lastDocTime ? "Load more" : "No more articles" // lastDoc if using single collection
							}
						</button>
					</div>
				)}
			</main>
		</div>
	);
}
