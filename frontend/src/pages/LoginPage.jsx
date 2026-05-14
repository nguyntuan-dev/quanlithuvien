import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { Eye, EyeOff, Home, Lock, Mail } from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuth } from '../hooks/useAuth'
import { authApi } from '../services/api'

const loginHeroImage = 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=1200&q=80'

export default function LoginPage() {
  const { user, loading, login, readerLogin } = useAuth()
  const navigate = useNavigate()
  const [mode, setMode] = useState('reader')
  const [email, setEmail] = useState('')
  const [matKhau, setMatKhau] = useState('')
  const [confirm, setConfirm] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [savingPassword, setSavingPassword] = useState(false)

  if (user) return <Navigate to="/" replace />

  const isChangePassword = mode === 'change-password'

  const resetForm = (nextMode) => {
    setMode(nextMode)
    setMatKhau('')
    setConfirm('')
    setShowPassword(false)
  }

  const changePassword = async () => {
    if (!email.trim()) {
      toast.error('Vui lòng nhập email')
      return false
    }
    if (matKhau.length < 6) {
      toast.error('Mật khẩu mới phải có ít nhất 6 ký tự')
      return false
    }
    if (matKhau !== confirm) {
      toast.error('Mật khẩu xác nhận chưa khớp')
      return false
    }

    setSavingPassword(true)
    try {
      await authApi.changePassword({
        email: email.trim(),
        mat_khau_moi: matKhau,
      })
      toast.success('Đổi mật khẩu thành công')
      resetForm('reader')
      return true
    } catch {
      return false
    } finally {
      setSavingPassword(false)
    }
  }

  const submit = async (e) => {
    e.preventDefault()

    if (isChangePassword) {
      await changePassword()
      return
    }

    let ok = await readerLogin(email.trim(), matKhau, { silent: true })
    if (!ok) ok = await login(email.trim(), matKhau, { silent: true })
    if (!ok) toast.error('Email hoặc mật khẩu không chính xác')
    if (ok) navigate('/', { replace: true })
  }

  const title = isChangePassword ? 'Đổi mật khẩu' : 'Đăng nhập Thư Viện'
  const description = isChangePassword
    ? 'Nhập email tài khoản và mật khẩu mới để cập nhật thông tin đăng nhập.'
    : 'Đăng nhập để quản lý tài khoản, theo dõi lịch sử mượn và sử dụng hệ thống thư viện.'

  return (
    <div className="min-h-screen bg-[#f6f6f4] text-[#2f2f2f] lg:grid lg:grid-cols-2">
      <button
        type="button"
        onClick={() => resetForm('reader')}
        className="absolute left-3 top-3 z-10 text-[#dfd08b] transition hover:text-[#c8b95f]"
        aria-label="Về đăng nhập độc giả"
      >
        <Home size={18} fill="currentColor" />
      </button>

      <section className="flex min-h-screen items-center justify-center px-6 py-10">
        <div className="w-full max-w-[360px]">
          <div className="mb-6">
            <h1 className="text-2xl font-semibold tracking-normal text-[#232323]">{title}</h1>
            <p className="mt-2 max-w-[320px] text-xs leading-5 text-[#aaa7a2]">{description}</p>
          </div>

          <form onSubmit={submit} className="space-y-4">
            <div>
              <label className="mb-1.5 block text-xs font-semibold text-[#5a554c]">Email</label>
              <div className="relative">
                <Mail size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#bbb4a8]" />
                <input
                  className="h-12 w-full rounded border border-[#e9edf5] bg-[#eef5ff] px-9 text-sm shadow-sm outline-none transition focus:border-[#d8ca91] focus:ring-2 focus:ring-[#e6d99b]/30"
                  type="email"
                  placeholder="example@email.com"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            <div>
              <label className="mb-1.5 block text-xs font-semibold text-[#5a554c]">
                {isChangePassword ? 'Mật khẩu mới' : 'Mật khẩu'}
              </label>
              <div className="relative">
                <Lock size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#bbb4a8]" />
                <input
                  className="h-12 w-full rounded border border-[#e9edf5] bg-[#eef5ff] px-9 pr-10 text-sm shadow-sm outline-none transition focus:border-[#d8ca91] focus:ring-2 focus:ring-[#e6d99b]/30"
                  type={showPassword ? 'text' : 'password'}
                  placeholder={isChangePassword ? 'Nhập mật khẩu mới' : 'Nhập mật khẩu'}
                  value={matKhau}
                  onChange={e => setMatKhau(e.target.value)}
                  required
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-[#a8a18f]"
                  onClick={() => setShowPassword(v => !v)}
                  aria-label={showPassword ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'}
                >
                  {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </div>

            {isChangePassword && (
              <div>
                <label className="mb-1.5 block text-xs font-semibold text-[#5a554c]">Xác nhận mật khẩu</label>
                <div className="relative">
                  <Lock size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#bbb4a8]" />
                  <input
                    className="h-11 w-full rounded border border-[#eeeae1] bg-white px-9 text-sm shadow-sm outline-none transition focus:border-[#d8ca91] focus:ring-2 focus:ring-[#e6d99b]/30"
                    type={showPassword ? 'text' : 'password'}
                    placeholder="Nhập lại mật khẩu"
                    value={confirm}
                    onChange={e => setConfirm(e.target.value)}
                    required
                  />
                </div>
              </div>
            )}

            <div className="flex items-center justify-between pt-1 text-xs text-[#969083]">
              <label className="flex items-center gap-2">
                <input type="checkbox" className="h-4 w-4 accent-[#d9ca91]" checked={showPassword} onChange={() => setShowPassword(v => !v)} />
                Hiện mật khẩu
              </label>
              {!isChangePassword && (
                <button type="button" className="text-[#8b867d] underline-offset-2 hover:text-[#b69b32] hover:underline" onClick={() => resetForm('change-password')}>
                  Đổi mật khẩu
                </button>
              )}
            </div>

            {!isChangePassword && (
              <div className="pt-1 text-center text-xs text-[#b2ada5]">
                Chưa có tài khoản?{' '}
                <Link className="font-medium text-[#b69b32] underline-offset-2 hover:underline" to="/register">
                  Đăng ký
                </Link>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || savingPassword}
              className="mt-2 h-12 w-full rounded bg-[#ded08a] text-sm font-semibold text-white shadow-sm transition hover:bg-[#d2c175] disabled:opacity-60"
            >
              {loading || savingPassword ? 'Đang xử lý...' : isChangePassword ? 'Cập nhật mật khẩu' : 'Đăng nhập'}
            </button>

            {isChangePassword && (
              <div className="pt-1 text-center text-xs text-[#9e978a]">
                <button type="button" className="text-[#b69b32] underline-offset-2 hover:underline" onClick={() => resetForm('reader')}>
                  Quay lại đăng nhập
                </button>
              </div>
            )}
          </form>
        </div>
      </section>

      <section className="hidden min-h-screen bg-[#cdb397] lg:block">
        <img
          src={loginHeroImage}
          alt="Sách đặt trên bàn gỗ"
          className="h-screen w-full object-cover"
        />
      </section>
    </div>
  )
}
