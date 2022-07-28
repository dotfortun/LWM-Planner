import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";

import { Home } from "./pages/home";
import injectContext from "./store/appContext";

import { Navigation } from "./component/navigation";
import { Footer } from "./component/footer";
import { ProfilePage } from "./pages/profile";
import { PilotPage } from "./pages/pilots";
import { MissionPage } from "./pages/mission";

//create your first component
const Layout = () => {
  //the basename is used when your project is published in a subdirectory and not in the root of the domain
  // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
  const basename = process.env.BASENAME || "";

  return (
    <div>
      <BrowserRouter basename={basename}>
        <ScrollToTop>
          <Navigation />
          <Routes>
            <Route element={<Home />} path="/" />
            <Route element={<ProfilePage />} path="/profile" />
            <Route element={<PilotPage />} path="/profile/pilots" />
            <Route element={<MissionPage />} path="/missions/:id" />
          </Routes>
          <Footer />
        </ScrollToTop>
      </BrowserRouter>
    </div>
  );
};

export default injectContext(Layout);
