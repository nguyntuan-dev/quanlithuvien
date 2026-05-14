import { createContext, useContext, useState, useEffect } from 'react'
import { authApi } from '../services/api'
import toast from 'react-hot-toast'

const AuthCtx = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem('user')
      const token = localStorage.getItem('token')
      return stored && token ? JSON.parse(stored) : null
    } catch {
      return null
    }
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    if (!token || !storedUser) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      setUser(null)
    }
  }, [])

  const login = async (email, mat_khau, options = {}) => {
    setLoading(true)
    try {
      const { data } = await authApi.login({ email, mat_khau })
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.nhan_vien))
      setUser(data.nhan_vien)
      toast.success(`✓ Đăng nhập thành công - Chào mừng ${data.nhan_vien.ho_ten}!`)
      return true
    } catch {
      if (!options.silent) toast.error('Email hoặc mật khẩu không chính xác')
      return false
    }
    finally { setLoading(false) }
  }

  const readerLogin = async (email, mat_khau, options = {}) => {
    setLoading(true)
    try {
      const { data } = await authApi.readerLogin({ email, mat_khau })
      const reader = { ...data.doc_gia, vai_tro: 'doc_gia', la_admin: false }
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(reader))
      setUser(reader)
      toast.success('Đăng nhập độc giả thành công')
      return true
    } catch {
      if (!options.silent) toast.error('Email hoặc mật khẩu không chính xác')
      return false
    } finally { setLoading(false) }
  }

  const readerSignup = async (payload) => {
    setLoading(true)
    try {
      const { data } = await authApi.readerSignup(payload)
      const reader = { ...data.doc_gia, vai_tro: 'doc_gia', la_admin: false }
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(reader))
      setUser(reader)
      toast.success('Đăng ký độc giả thành công')
      return true
    } catch {
      return false
    } finally { setLoading(false) }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    toast.success('✓ Đã đăng xuất')
  }

  const updateUser = (patch) => {
    setUser(prev => {
      if (!prev) return prev
      const next = { ...prev, ...patch }
      localStorage.setItem('user', JSON.stringify(next))
      return next
    })
  }

  return (
    <AuthCtx.Provider value={{ user, loading, login, readerLogin, readerSignup, logout, updateUser }}>
      {children}
    </AuthCtx.Provider>
  )
}

export const useAuth = () => useContext(AuthCtx)
