import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Layout from "./modules/Layout";
import MapTab from "./modules/navbar/tabs/MapTab";

function App() {
  return (
    <BrowserRouter>
        <Layout>
            <Routes>
                <Route path={'/'} element={<div>Welcome to the flood and drought prediction system</div>}/>
                <Route path={'/map'} element={<MapTab />} />
            </Routes>
        </Layout>
    </BrowserRouter>
  )
}

export default App
