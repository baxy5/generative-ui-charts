"use client";

import React, { Fragment, useRef } from "react";

const IframeLoader = () => {
  const IFRAME_HEIGHT = 650;
  const urls = useRef<string[]>([
    "https://pub-b348006f0b2142f7a105983d74576412.r2.dev/4c8dd9016315/index.html",
    "https://pub-b348006f0b2142f7a105983d74576412.r2.dev/640abbc33b5c/index.html",
    "https://pub-b348006f0b2142f7a105983d74576412.r2.dev/e25523448e7c/index.html",
  ]);

  return (
    <div>
      <h2 className="text-center">Which layout do you prefer?</h2>
      <div className="flex flex-col items-center gap-4">
        {urls &&
          urls.current.map((url: string) => (
            <Fragment key={url}>
              <div>
                <button className="border-2 border-white rounded-lg px-4 py-2 cursor-pointer font-bold uppercase hover:bg-white hover:text-blue-900">
                  Choose
                </button>
              </div>
              <figure className="relative aspect-[16/9] w-1/2 overflow-hidden rounded-lg border shadow-sm">
                <iframe
                  src={url}
                  title="Generated Component"
                  sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox allow-forms"
                  width="1200px"
                  height={IFRAME_HEIGHT}
                  loading="eager"
                  className="absolute left-0 top-0 origin-top-left"
                  style={{
                    colorScheme: "normal",
                    border: "none",
                    transform: "scale(0.615)",
                  }}
                ></iframe>
              </figure>
            </Fragment>
          ))}
      </div>
    </div>
  );
};

export default IframeLoader;
