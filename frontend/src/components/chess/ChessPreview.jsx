import { Chessboard } from "react-chessboard";

export default function ChessPreview({ fen }) {
  return (
    <div className="mx-auto w-full max-w-[520px] rounded-3xl border border-slate-700 bg-slate-950 p-4 shadow-2xl shadow-blue-950/30">
      <Chessboard
        position={fen || "start"}
        boardWidth={480}
        arePiecesDraggable={false}
      />
    </div>
  );
}
