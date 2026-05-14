import { useEffect, useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { PageHeader, Badge, Modal, Field, Input, Select } from '../components/UI'
import { User, Mail, Phone, BookOpen, Heart, Facebook, Twitter, Instagram, Pencil, Lock } from 'lucide-react'
import { authApi, muonTraApi, yeuThichApi } from '../services/api'
import toast from 'react-hot-toast'

const GIOI_TINH_OPTS = [
  { value: '', label: '— Chưa chọn —' },
  { value: 'NAM', label: 'Nam' },
  { value: 'NU', label: 'Nữ' },
  { value: 'KHAC', label: 'Khác' },
]

export default function ProfilePage() {
  const { user, updateUser } = useAuth()
  const isReader = user?.vai_tro === 'doc_gia'

  const [profileOpen, setProfileOpen] = useState(false)
  const [passwordOpen, setPasswordOpen] = useState(false)
  const [savingProfile, setSavingProfile] = useState(false)
  const [savingPassword, setSavingPassword] = useState(false)

  const [borrowing, setBorrowing] = useState(0)
  const [favCount, setFavCount] = useState(0)

  const [profileForm, setProfileForm] = useState({
    ho_ten: '',
    email: '',
    so_dien_thoai: '',
    dia_chi: '',
    ngay_sinh: '',
    gioi_tinh: '',
  })
  const [staffForm, setStaffForm] = useState({ ho_ten: '', so_dien_thoai: '' })

  const [pwForm, setPwForm] = useState({ cu: '', moi: '', xac_nhan: '' })

  useEffect(() => {
    if (!user || !isReader) return
    let cancelled = false
    ;(async () => {
      try {
        const [hist, favs] = await Promise.all([
          muonTraApi.lichSu(user.ma_doc_gia),
          yeuThichApi.list(),
        ])
        if (cancelled) return
        const active = (hist.data || []).filter(
          p => p.trang_thai === 'dang_muon' || p.trang_thai === 'qua_han'
        ).length
        setBorrowing(active)
        setFavCount((favs.data || []).length)
      } catch {
        if (!cancelled) {
          setBorrowing(0)
          setFavCount(0)
        }
      }
    })()
    return () => { cancelled = true }
  }, [user, isReader])

  useEffect(() => {
    if (!profileOpen || !user) return
    if (isReader) {
      setProfileForm({
        ho_ten: user.ho_ten || '',
        email: user.email || '',
        so_dien_thoai: user.so_dien_thoai || '',
        dia_chi: user.dia_chi || '',
        ngay_sinh: user.ngay_sinh ? String(user.ngay_sinh).slice(0, 10) : '',
        gioi_tinh: user.gioi_tinh || '',
      })
    } else {
      setStaffForm({
        ho_ten: user.ho_ten || '',
        so_dien_thoai: user.so_dien_thoai || '',
      })
    }
  }, [profileOpen, user, isReader])

  useEffect(() => {
    if (!passwordOpen) return
    setPwForm({ cu: '', moi: '', xac_nhan: '' })
  }, [passwordOpen])

  const pf = (k) => (e) => setProfileForm(s => ({ ...s, [k]: e.target.value }))
  const sf = (k) => (e) => setStaffForm(s => ({ ...s, [k]: e.target.value }))
  const wf = (k) => (e) => setPwForm(s => ({ ...s, [k]: e.target.value }))

  const openProfile = () => setProfileOpen(true)

  const saveProfile = async () => {
    if (isReader) {
      if (!profileForm.ho_ten.trim()) {
        toast.error('Vui lòng nhập họ tên')
        return
      }
      if (!profileForm.email.trim()) {
        toast.error('Vui lòng nhập email')
        return
      }
      setSavingProfile(true)
      try {
        const body = {
          ho_ten: profileForm.ho_ten.trim(),
          email: profileForm.email.trim(),
          so_dien_thoai: profileForm.so_dien_thoai.trim() || undefined,
          dia_chi: profileForm.dia_chi.trim() || undefined,
        }
        if (profileForm.ngay_sinh) body.ngay_sinh = profileForm.ngay_sinh
        if (profileForm.gioi_tinh) body.gioi_tinh = profileForm.gioi_tinh
        const { data } = await authApi.updateMyReaderProfile(body)
        updateUser({ ...data, vai_tro: 'doc_gia', la_admin: false })
        toast.success('Đã cập nhật hồ sơ')
        setProfileOpen(false)
      } catch {
        /* toast từ interceptor */
      } finally {
        setSavingProfile(false)
      }
    } else {
      if (!staffForm.ho_ten.trim()) {
        toast.error('Vui lòng nhập họ tên')
        return
      }
      setSavingProfile(true)
      try {
        const { data } = await authApi.updateMyStaffProfile({
          ho_ten: staffForm.ho_ten.trim(),
          so_dien_thoai: staffForm.so_dien_thoai.trim() || undefined,
        })
        updateUser(data)
        toast.success('Đã cập nhật hồ sơ')
        setProfileOpen(false)
      } catch {
        /* toast từ interceptor */
      } finally {
        setSavingProfile(false)
      }
    }
  }

  const savePassword = async () => {
    if (!pwForm.cu) {
      toast.error('Nhập mật khẩu hiện tại')
      return
    }
    if (pwForm.moi.length < 6) {
      toast.error('Mật khẩu mới ít nhất 6 ký tự')
      return
    }
    if (pwForm.moi !== pwForm.xac_nhan) {
      toast.error('Xác nhận mật khẩu không khớp')
      return
    }
    setSavingPassword(true)
    try {
      await authApi.changeMyPassword({ mat_khau_cu: pwForm.cu, mat_khau_moi: pwForm.moi })
      toast.success('Đã đổi mật khẩu')
      setPasswordOpen(false)
    } catch {
      /* toast từ interceptor */
    } finally {
      setSavingPassword(false)
    }
  }

  return (
    <div>
      <PageHeader title="Thông tin tài khoản" subtitle="Quản lý thông tin cá nhân và bảo mật" />

      <div className="px-6 flex justify-center mt-4">
        <div className="w-full max-w-3xl bg-surface rounded-2xl shadow-xl overflow-hidden flex flex-col md:flex-row border border-border">

          <div className="w-full md:w-1/3 bg-gradient-to-br from-[#ffd89b] to-[#19033d] p-8 flex flex-col items-center justify-center text-white relative">
            <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]" />

            <div className="relative mb-6 group">
              <div className="w-24 h-24 rounded-full border-4 border-white/30 overflow-hidden shadow-2xl transition-transform group-hover:scale-105">
                <img
                  src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(user?.ho_ten || 'user')}`}
                  alt="Avatar"
                  className="w-full h-full object-cover bg-primary-light"
                />
              </div>
              <button
                type="button"
                onClick={openProfile}
                className="absolute bottom-0 right-0 p-1.5 bg-white text-primary rounded-full shadow-lg hover:bg-surface-muted transition-colors"
                aria-label="Chỉnh sửa hồ sơ"
              >
                <Pencil size={12} />
              </button>
            </div>

            <h2 className="text-xl font-bold mb-1 drop-shadow-md">{user?.ho_ten}</h2>
            <p className="text-white/70 text-sm mb-6 font-medium tracking-wide uppercase">
              {isReader ? 'Độc giả' : (user?.chuc_vu || 'Nhân viên')}
            </p>

            <div className="space-y-3 w-full">
              <button
                type="button"
                onClick={openProfile}
                className="w-full flex items-center gap-2 px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-sm font-medium transition-all backdrop-blur-sm border border-white/10"
              >
                <Pencil size={14} /> Chỉnh sửa hồ sơ
              </button>
              <button
                type="button"
                onClick={() => setPasswordOpen(true)}
                className="w-full flex items-center gap-2 px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-sm font-medium transition-all backdrop-blur-sm border border-white/10"
              >
                <Lock size={14} /> Đổi mật khẩu
              </button>
            </div>
          </div>

          <div className="flex-1 p-8 bg-surface">
            <div className="mb-8">
              <div className="flex items-center justify-between border-b border-border pb-2 mb-4">
                <h3 className="text-sm font-bold uppercase tracking-widest text-ink-faint">Thông tin cơ bản</h3>
                <Badge variant="blue">Cá nhân</Badge>
              </div>

              <div className="grid grid-cols-2 gap-y-6 gap-x-4">
                <div>
                  <label className="text-[10px] uppercase font-bold text-ink-faint mb-1 block">Email</label>
                  <div className="flex items-center gap-2 text-sm text-ink-muted">
                    <Mail size={14} className="text-primary shrink-0" />
                    <span className="truncate">{user?.email || 'Chưa cập nhật'}</span>
                  </div>
                </div>
                <div>
                  <label className="text-[10px] uppercase font-bold text-ink-faint mb-1 block">Số điện thoại</label>
                  <div className="flex items-center gap-2 text-sm text-ink-muted">
                    <Phone size={14} className="text-primary shrink-0" />
                    <span>{user?.so_dien_thoai || 'Chưa cập nhật'}</span>
                  </div>
                </div>
                <div>
                  <label className="text-[10px] uppercase font-bold text-ink-faint mb-1 block">Mã định danh</label>
                  <div className="flex items-center gap-2 text-sm font-mono text-ink-muted">
                    <User size={14} className="text-primary shrink-0" />
                    <span>{user?.ma_doc_gia || user?.ma_nhan_vien}</span>
                  </div>
                </div>
              </div>
            </div>

            {isReader && (
              <div className="mb-8">
                <div className="flex items-center justify-between border-b border-border pb-2 mb-4">
                  <h3 className="text-sm font-bold uppercase tracking-widest text-ink-faint">Hoạt động</h3>
                  <Badge variant="green">Gần đây</Badge>
                </div>

                <div className="grid grid-cols-2 gap-y-6 gap-x-4">
                  <div>
                    <label className="text-[10px] uppercase font-bold text-ink-faint mb-1 block">Đang mượn</label>
                    <div className="flex items-center gap-2 text-xl font-bold text-primary">
                      <BookOpen size={18} />
                      <span>{borrowing}</span>
                    </div>
                  </div>
                  <div>
                    <label className="text-[10px] uppercase font-bold text-ink-faint mb-1 block">Yêu thích</label>
                    <div className="flex items-center gap-2 text-xl font-bold text-danger">
                      <Heart size={18} />
                      <span>{favCount}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div className="flex gap-4 pt-4 border-t border-border mt-auto">
              <button type="button" className="text-ink-faint hover:text-primary transition-colors" aria-label="Facebook"><Facebook size={18} /></button>
              <button type="button" className="text-ink-faint hover:text-primary transition-colors" aria-label="Twitter"><Twitter size={18} /></button>
              <button type="button" className="text-ink-faint hover:text-primary transition-colors" aria-label="Instagram"><Instagram size={18} /></button>
            </div>
          </div>

        </div>
      </div>

      <Modal
        open={profileOpen}
        onClose={() => setProfileOpen(false)}
        title={isReader ? 'Chỉnh sửa hồ sơ độc giả' : 'Chỉnh sửa hồ sơ'}
        size="md"
        footer={(
          <div className="flex justify-end gap-2">
            <button type="button" className="btn btn-ghost" onClick={() => setProfileOpen(false)}>Hủy</button>
            <button type="button" className="btn btn-primary" disabled={savingProfile} onClick={saveProfile}>
              {savingProfile ? 'Đang lưu…' : 'Lưu thay đổi'}
            </button>
          </div>
        )}
      >
        {isReader ? (
          <div className="space-y-4">
            <Field label="Họ và tên" required><Input value={profileForm.ho_ten} onChange={pf('ho_ten')} /></Field>
            <Field label="Email" required><Input type="email" value={profileForm.email} onChange={pf('email')} /></Field>
            <Field label="Số điện thoại"><Input value={profileForm.so_dien_thoai} onChange={pf('so_dien_thoai')} /></Field>
            <Field label="Địa chỉ"><Input value={profileForm.dia_chi} onChange={pf('dia_chi')} /></Field>
            <Field label="Ngày sinh"><Input type="date" value={profileForm.ngay_sinh} onChange={pf('ngay_sinh')} /></Field>
            <Field label="Giới tính">
              <Select value={profileForm.gioi_tinh} onChange={pf('gioi_tinh')}>
                {GIOI_TINH_OPTS.map(o => (
                  <option key={o.value || 'x'} value={o.value}>{o.label}</option>
                ))}
              </Select>
            </Field>
          </div>
        ) : (
          <div className="space-y-4">
            <Field label="Họ và tên" required><Input value={staffForm.ho_ten} onChange={sf('ho_ten')} /></Field>
            <Field label="Số điện thoại"><Input value={staffForm.so_dien_thoai} onChange={sf('so_dien_thoai')} /></Field>
            <p className="text-xs text-ink-muted">Email và chức vụ chỉ có thể thay đổi qua quản trị viên.</p>
          </div>
        )}
      </Modal>

      <Modal
        open={passwordOpen}
        onClose={() => setPasswordOpen(false)}
        title="Đổi mật khẩu"
        size="sm"
        footer={(
          <div className="flex justify-end gap-2">
            <button type="button" className="btn btn-ghost" onClick={() => setPasswordOpen(false)}>Hủy</button>
            <button type="button" className="btn btn-primary" disabled={savingPassword} onClick={savePassword}>
              {savingPassword ? 'Đang lưu…' : 'Đổi mật khẩu'}
            </button>
          </div>
        )}
      >
        <div className="space-y-4">
          <Field label="Mật khẩu hiện tại" required>
            <Input type="password" autoComplete="current-password" value={pwForm.cu} onChange={wf('cu')} />
          </Field>
          <Field label="Mật khẩu mới" required>
            <Input type="password" autoComplete="new-password" value={pwForm.moi} onChange={wf('moi')} />
          </Field>
          <Field label="Nhập lại mật khẩu mới" required>
            <Input type="password" autoComplete="new-password" value={pwForm.xac_nhan} onChange={wf('xac_nhan')} />
          </Field>
        </div>
      </Modal>
    </div>
  )
}
