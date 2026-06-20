import { useEffect, useState } from "react";
import { useTimeline } from "./hooks/useTimeline";
import Loading from "./components/Loading";
import ErrorPage from "./components/Error";

export default function App() {
  const { data, loading, error } = useTimeline();
  const [index, setIndex] = useState(0);
  const [query, setQuery] = useState("");

  const viewData = data.filter((item) => {
    const q = query.toLowerCase();
    if (!q) return true;

    return (
      item.window_title?.toLowerCase().includes(q) ||
      item.app_name?.toLowerCase().includes(q)
    );
  });

  const safeIndex = viewData.length ? Math.min(index, viewData.length - 1) : 0;

  const current = viewData.length > 0 ? viewData[safeIndex] : viewData[0]; // fallback safety

  // Keyboard navigation
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight") {
        setIndex((i) => Math.min(i + 1, viewData.length - 1));
      }

      if (e.key === "ArrowLeft") {
        setIndex((i) => Math.max(i - 1, 0));
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [viewData.length]);

  const filename = current?.image_path?.split("/").pop();

  if (loading) return <Loading />;
  if (error) return <ErrorPage />;

  return (
    <div className="h-screen w-screen overflow-hidden bg-linear-to-b from-black via-zinc-950 to-black text-white flex items-center justify-center p-1.25px">
      {/* Vignette overlay */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle,transparent_40%,black_100%)]" />
      <div className="relative z-10 w-[90vw] h-[90vh] flex flex-col">
        {/* Title */}
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-semibold tracking-wide">Memoria</h1>
          <div className="mt-1 text-xs text-zinc-500">
            v0.1.0 • Search your past.
          </div>
        </div>
        {/* Header info */}
        <div className="mb-4 text-center">
          {viewData.length === 0 ? (
            <div className="text-lg font-medium text-zinc-400">
              No results found
            </div>
          ) : (
            <>
              <div className="text-lg font-medium">
                {current.app_name || "Unknown App"}
              </div>
              <div className="text-sm text-zinc-400">
                {current.window_title}
              </div>
            </>
          )}
        </div>
        {/* Search */}
        <input
          className="w-full max-w-none px-4 py-2 rounded-lg bg-zinc-900 border border-zinc-800 text-sm focus:outline-none focus:border-zinc-600"
          placeholder="Search memory..."
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIndex(0);
          }}
        />

        {/* Slider */}
        <input
          type="range"
          min={0}
          max={Math.max(0, viewData.length - 1)}
          value={index}
          onChange={(e) => setIndex(Number(e.target.value))}
          disabled={viewData.length === 0}
          className="w-full mt-4 accent-zinc-400"
        />

        {/* Timestamp */}
        <div className="mt-10 text-zinc-400 text-sm">
          {current?.timestamp
            ? new Date(current.timestamp).toLocaleString()
            : ""}
        </div>

        {/* Divider */}
        <div className="w-full border-t border-zinc-800 my-4" />

        {/* Screenshot */}
        <img
          src={`http://localhost:8009/screenshots/${filename}`}
          className="block w-full max-h-[60vh] object-contain rounded-xl border border-zinc-800 shadow-xl bg-black"
        />
      </div>
    </div>
  );
}
