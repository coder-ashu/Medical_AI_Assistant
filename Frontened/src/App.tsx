import Chat from "./chat";
import { Loading } from "./components/loading";
import { useState, useEffect } from "react";
import Lottie from "lottie-react";
import chatbotAnim from "./assets/chatbot.json";

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 2000);
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <Loading />;
  }
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-black text-black p-6">
      <h1 className="text-3xl font-bold mb-4">
        Welcome to Medical AI Assistant
      </h1>
      <Lottie
        animationData={chatbotAnim}
        loop
        autoplay
        className="w-60 h-60 mb-6"
      />
      <Chat />
    </div>
  );
}

export default App;
