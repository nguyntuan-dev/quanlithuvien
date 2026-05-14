import { useEffect, useState } from 'react'
import { heThongApi } from '../services/api'
import { PageHeader, Field, Input, Spinner, Empty } from '../components/UI'
import toast from 'react-hot-toast'

export default function HeThongPage() {
  const [settings, setSettings] = useState([])
  const [logs, setLogs] = useState([])
  const [backup, setBackup] = useState('')
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    try {
      const [cauHinh, audit] = await Promise.all([
        heThongApi.cauHinh(),
        heThongApi.auditLog({ limit: 50 }),
      ])
      setSettings(cauHinh.data)
      setLogs(audit.data)
    } finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  const update = async (row, value) => {
    await heThongApi.updateCauHinh(row.khoa, { gia_tri: value, mo_ta: row.mo_ta })
    toast.success('Đã cập nhật cấu hình')
    load()
  }

  const makeBackup = async () => {
    const { data } = await heThongApi.backup()
    setBackup(JSON.stringify(data, null, 2))
    toast.success('Đã tạo backup JSON')
  }

  const restore = async () => {
    if (!backup.trim()) { toast.error('Chưa có JSON để phục hồi'); return }
    await heThongApi.restore(JSON.parse(backup))
    toast.success('Đã gửi dữ liệu restore')
    load()
  }

  return (
    <div>
      <PageHeader title="Hệ thống" subtitle="Cấu hình chính sách, backup/restore và audit log" />
      <div className="px-6 space-y-4">
        <div className="card p-4">
          <h2 className="text-sm font-semibold mb-3">Cấu hình chính sách mượn</h2>
          {loading ? <Spinner /> : settings.map(row => (
            <div key={row.khoa} className="grid grid-cols-[220px_1fr_120px] gap-3 items-end mb-3">
              <Field label={row.khoa}>
                <Input defaultValue={row.gia_tri} onBlur={e => update(row, e.target.value)} />
              </Field>
              <div className="text-sm text-ink-muted pb-2">{row.mo_ta}</div>
              <button className="btn btn-secondary" onClick={() => update(row, row.gia_tri)}>Lưu</button>
            </div>
          ))}
        </div>

        <div className="card p-4">
          <div className="flex justify-between items-center mb-3">
            <h2 className="text-sm font-semibold">Sao lưu / phục hồi dữ liệu</h2>
            <div className="flex gap-2">
              <button className="btn btn-secondary" onClick={makeBackup}>Tạo backup</button>
              <button className="btn btn-danger" onClick={restore}>Restore</button>
            </div>
          </div>
          <textarea className="input font-mono text-xs min-h-[180px]" value={backup} onChange={e => setBackup(e.target.value)} />
        </div>

        <div className="card overflow-hidden">
          <table className="w-full">
            <thead className="bg-surface-soft border-b border-border">
              <tr>
                <th className="th">Thời gian</th>
                <th className="th">Người dùng</th>
                <th className="th">Hành động</th>
                <th className="th">Đối tượng</th>
                <th className="th">Chi tiết</th>
              </tr>
            </thead>
            <tbody>
              {logs.length === 0 ? <tr><td colSpan={5}><Empty /></td></tr>
                : logs.map(log => (
                  <tr key={log.id} className="table-row">
                    <td className="td text-xs">{new Date(log.created_at).toLocaleString('vi-VN')}</td>
                    <td className="td">{log.nguoi_thuc_hien || '-'}</td>
                    <td className="td">{log.hanh_dong}</td>
                    <td className="td">{log.doi_tuong || '-'}</td>
                    <td className="td">{log.chi_tiet || '-'}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
