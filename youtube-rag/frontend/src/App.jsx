import { useState } from 'react';
import VideoInput from './components/VideoInput';
import ChatInterface from './components/ChatInterface';

function App() {
  const [videoProcessed, setVideoProcessed] = useState(false);

  return (
    <div className="min-h-screen bg-background p-4 md:p-8 flex items-center justify-center">
      {!videoProcessed ? (
        <VideoInput onVideoProcessed={() => setVideoProcessed(true)} />
      ) : (
        <ChatInterface />
      )}
    </div>
  );
}

export default App;
