import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider, theme } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import { QueryClient, QueryClientProvider } from 'react-query';
import 'antd/dist/reset.css';
import './App.css';

// 导入页面组件
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import ProjectList from './pages/ProjectList';
import ProjectDetail from './pages/ProjectDetail';
import CharacterList from './pages/CharacterList';
import FactionList from './pages/FactionList';
import PlotList from './pages/PlotList';

import ChapterDetail from './pages/ChapterDetail';
import WorldSettings from './pages/WorldSettings';
import CultivationSystems from './pages/CultivationSystems';
import Timeline from './pages/Timeline';
import Relations from './pages/Relations';
import AIAssistant from './pages/AIAssistant';
import Settings from './pages/Settings';
import AITest from './pages/AITest';
import OllamaTest from './pages/OllamaTest';
import ResourceDistribution from './pages/ResourceDistribution';
import RaceDistribution from './pages/RaceDistribution';
import SecretRealms from './pages/SecretRealms';
import EquipmentSystems from './pages/EquipmentSystems';
import PetSystems from './pages/PetSystems';
import MapStructure from './pages/MapStructure';
import DimensionStructure from './pages/DimensionStructure';
import SpiritualTreasureSystems from './pages/SpiritualTreasureSystems';
import CivilianSystems from './pages/CivilianSystems';
import JudicialSystems from './pages/JudicialSystems';
import ProfessionSystems from './pages/ProfessionSystems';
import VolumeManagement from './pages/VolumeManagement';
import ContentManagement from './pages/ContentManagement';
import SettingsManagement from './pages/SettingsManagement';

// 创建 React Query 客户端
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider
        locale={zhCN}
        theme={{
          algorithm: theme.defaultAlgorithm,
          token: {
            colorPrimary: '#1890ff',
            borderRadius: 6,
          },
        }}
      >
        <Router>
          <div className="App">
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/projects" element={<ProjectList />} />
                <Route path="/projects/:id" element={<ProjectDetail />} />
                <Route path="/projects/:id/volumes" element={<VolumeManagement />} />
                <Route path="/projects/:id/content" element={<ContentManagement />} />
                <Route path="/projects/:id/settings" element={<SettingsManagement />} />
                <Route path="/projects/:id/characters" element={<CharacterList />} />
                <Route path="/projects/:id/factions" element={<FactionList />} />
                <Route path="/projects/:id/plots" element={<PlotList />} />
                <Route path="/projects/:projectId/volumes/:volumeId/chapters/:chapterId" element={<ChapterDetail />} />
                <Route path="/projects/:id/world-settings" element={<WorldSettings />} />
                <Route path="/projects/:id/cultivation-systems" element={<CultivationSystems />} />
                <Route path="/projects/:id/timeline" element={<Timeline />} />
                <Route path="/projects/:id/relations" element={<Relations />} />
                <Route path="/projects/:id/resource-distribution" element={<ResourceDistribution />} />
                <Route path="/projects/:id/race-distribution" element={<RaceDistribution />} />
                <Route path="/projects/:id/secret-realms" element={<SecretRealms />} />
                <Route path="/projects/:id/equipment-systems" element={<EquipmentSystems />} />
                <Route path="/projects/:id/pet-systems" element={<PetSystems />} />
                <Route path="/projects/:id/map-structure" element={<MapStructure />} />
                <Route path="/projects/:id/dimension-structure" element={<DimensionStructure />} />
                <Route path="/projects/:id/spiritual-treasure-systems" element={<SpiritualTreasureSystems />} />
                <Route path="/projects/:id/civilian-systems" element={<CivilianSystems />} />
                <Route path="/projects/:id/judicial-systems" element={<JudicialSystems />} />
                <Route path="/projects/:id/profession-systems" element={<ProfessionSystems />} />
                <Route path="/ai-assistant" element={<AIAssistant />} />
                <Route path="/settings" element={<Settings />} />
                <Route path="/ai-test" element={<AITest />} />
                <Route path="/ollama-test" element={<OllamaTest />} />
              </Routes>
            </Layout>
          </div>
        </Router>
      </ConfigProvider>
    </QueryClientProvider>
  );
}

export default App;
