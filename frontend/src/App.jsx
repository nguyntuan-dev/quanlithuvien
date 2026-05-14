import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './hooks/useAuth'
import Layout from './components/Layout'
import DashboardPage from './pages/DashboardPage'
import CatalogPage from './pages/CatalogPage'
import TaiLieuPage from './pages/TaiLieuPage'
import DocGiaPage from './pages/DocGiaPage'
import MuonTraPage from './pages/MuonTraPage'
import DatTruocPage from './pages/DatTruocPage'
import ViPhamPage from './pages/ViPhamPage'
import NhanVienPage from './pages/NhanVienPage'
import ThongKePage from './pages/ThongKePage'
import LichSuPage from './pages/LichSuPage'
import HeThongPage from './pages/HeThongPage'
import ProfilePage from './pages/ProfilePage'
import FavoritePage from './pages/FavoritePage'
import UnauthorizedPage from './pages/UnauthorizedPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'

function ProtectedRoute({ children }) {
  const { user } = useAuth()
  return user ? children : <Navigate to="/login" replace />
}

function AdminRoute({ children }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return user.la_admin ? children : <Navigate to="/unauthorized" replace />
}

function StaffRoute({ children }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return user.vai_tro === 'doc_gia' ? <Navigate to="/unauthorized" replace /> : children
}

function HomeRoute() {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return user.vai_tro === 'doc_gia' ? <Navigate to="/tra-cuu" replace /> : <DashboardPage />
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/unauthorized" element={<UnauthorizedPage />} />
        <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route index element={<HomeRoute />} />
          <Route path="tra-cuu"   element={<CatalogPage />} />
          <Route path="tai-lieu"  element={<StaffRoute><TaiLieuPage /></StaffRoute>} />
          <Route path="doc-gia"   element={<StaffRoute><DocGiaPage /></StaffRoute>} />
          <Route path="muon-tra"  element={<StaffRoute><MuonTraPage /></StaffRoute>} />
          <Route path="dat-truoc" element={<StaffRoute><DatTruocPage /></StaffRoute>} />
          <Route path="vi-pham"   element={<StaffRoute><ViPhamPage /></StaffRoute>} />
          <Route path="nhan-vien" element={<AdminRoute><NhanVienPage /></AdminRoute>} />
          <Route path="lich-su"   element={<LichSuPage />} />
          <Route path="profile"   element={<ProfilePage />} />
          <Route path="yeu-thich" element={<FavoritePage />} />
          <Route path="thong-ke"  element={<StaffRoute><ThongKePage /></StaffRoute>} />
          <Route path="he-thong"  element={<AdminRoute><HeThongPage /></AdminRoute>} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  )
}
