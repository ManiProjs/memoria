import { useEffect, useState } from "react";
import { api } from "../lib/api";

export type Snapshot = {
  id: number;
  timestamp: string;
  app_name: string | null;
  window_title: string | null;
  image_path: string;
};

export function useTimeline() {
  const [data, setData] = useState<Snapshot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .get<Snapshot[]>("/timeline")
      .then((res) => {
        setData(res.data);
        setError(null);
      })
      .catch((err) => {
        console.error(err);
        setError("Connection failed");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return { data, loading, error };
}
