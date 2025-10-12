import { useEffect, useRef, useState } from "react";
import { Scene1 } from "@/components/presentation/Scene1";
import { Scene2 } from "@/components/presentation/Scene2";
import { Scene3 } from "@/components/presentation/Scene3";
import { Scene4 } from "@/components/presentation/Scene4";
import { Scene5 } from "@/components/presentation/Scene5";
import { Scene6 } from "@/components/presentation/Scene6";
import { Scene7 } from "@/components/presentation/Scene7";
import { Scene8 } from "@/components/presentation/Scene8";
import { Scene9 } from "@/components/presentation/Scene9";
import { PresentationNav } from "@/components/presentation/PresentationNav";

const Presentation = () => {
  const [activeScene, setActiveScene] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);

  const scenes = [
    { id: 0, name: "Home", component: Scene1 },
    { id: 1, name: "Problem", component: Scene2 },
    { id: 2, name: "Solution", component: Scene3 },
    { id: 3, name: "How It Works", component: Scene4 },
    { id: 4, name: "Results", component: Scene5 },
    { id: 5, name: "Vision", component: Scene6 },
    { id: 6, name: "Impact", component: Scene7 },
    { id: 7, name: "Roadmap", component: Scene8 },
    { id: 8, name: "Closing", component: Scene9 },
  ];

  useEffect(() => {
    const handleScroll = () => {
      if (!containerRef.current) return;
      const scrollPosition = containerRef.current.scrollTop;
      const windowHeight = window.innerHeight;
      const currentScene = Math.round(scrollPosition / windowHeight);
      setActiveScene(currentScene);
    };

    const container = containerRef.current;
    if (container) {
      container.addEventListener("scroll", handleScroll);
      return () => container.removeEventListener("scroll", handleScroll);
    }
  }, []);

  const scrollToScene = (sceneId: number) => {
    if (!containerRef.current) return;
    const windowHeight = window.innerHeight;
    containerRef.current.scrollTo({
      top: sceneId * windowHeight,
      behavior: "smooth",
    });
  };

  return (
    <div className="relative w-full h-screen overflow-hidden bg-background">
      <PresentationNav
        scenes={scenes}
        activeScene={activeScene}
        onNavigate={scrollToScene}
      />
      
      <div
        ref={containerRef}
        className="h-screen overflow-y-scroll snap-y snap-mandatory scroll-smooth"
        style={{ scrollbarWidth: "none", msOverflowStyle: "none" }}
      >
        <style>{`::-webkit-scrollbar { display: none; }`}</style>
        {scenes.map((scene) => {
          const SceneComponent = scene.component;
          return (
            <section
              key={scene.id}
              className="h-screen w-full snap-start snap-always flex items-center justify-center"
            >
              <SceneComponent />
            </section>
          );
        })}
      </div>
    </div>
  );
};

export default Presentation;
