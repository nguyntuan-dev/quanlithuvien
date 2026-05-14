import { useEffect, useState } from 'react'
import { thongKeApi } from '../services/api'
import { StatCard, Spinner } from '../components/UI'
import { PageHeader } from '../components/UI'
import { BookOpen, Users, Clock, AlertTriangle, CheckCircle } from 'lucide-react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts'

export default function DashboardPage() {
  const [stats, setStats]     = useState(null)
  const [chart, setChart]     = useState([])
  const [top, setTop]         = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      thongKeApi.tongQuan(),
      thongKeApi.muonTheoThang(),
      thongKeApi.topTaiLieu(),
    ]).then(([s, c, t]) => {
      setStats(s.data)
      setChart(c.data)
      setTop(t.data)
    }).finally(() => setLoading(false))
  }, [])

  if (loading) return <Spinner />

  return (
    <div>
      <PageHeader title="Tổng quan" subtitle="Tình hình hoạt động thư viện" />

      <div className="px-6 space-y-6">
        {/* Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
          <StatCard label="Tổng tài liệu"       value={stats?.tong_tai_lieu?.toLocaleString()}  icon={BookOpen}     color="blue"  />
          <StatCard label="Độc giả hoạt động"   value={stats?.doc_gia_hoat_dong?.toLocaleString()} icon={Users}     color="green" />
          <StatCard label="Đang được mượn"      value={stats?.dang_duoc_muon?.toLocaleString()}  icon={CheckCircle}  color="default"/>
          <StatCard label="Đang chờ duyệt"      value={stats?.dat_truoc_cho_duyet?.toLocaleString()} icon={Clock} color="yellow" />
          <StatCard
            label="Vi phạm chưa xử lý"
            value={stats?.vi_pham_chua_xu_ly?.toLocaleString()}
            sub={`Tiền phạt: ${(stats?.tong_tien_phat_chua_thu || 0).toLocaleString('vi-VN')}đ`}
            icon={AlertTriangle} color="red"
          />
        </div>

        <div className="grid lg:grid-cols-2 gap-4">
          {/* Biểu đồ mượn theo tháng */}
          <div className="card p-5">
            <h3 className="section-title">Lượt mượn theo tháng</h3>
            {chart.length === 0
              ? <p className="text-sm text-ink-faint text-center py-10">Chưa có dữ liệu</p>
              : <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={chart} barSize={24}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="thang" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Bar dataKey="so_luong" fill="#1a56db" radius={[4,4,0,0]} name="Lượt mượn" />
                  </BarChart>
                </ResponsiveContainer>
            }
          </div>

          {/* Top tài liệu */}
          <div className="card p-5">
            <h3 className="section-title">Top tài liệu được mượn nhiều nhất</h3>
            {top.length === 0
              ? <p className="text-sm text-ink-faint text-center py-10">Chưa có dữ liệu</p>
              : <div className="space-y-3">
                  {top.slice(0,7).map((item, i) => (
                    <div key={i} className="flex items-center gap-3">
                      <span className="text-xs font-mono text-ink-faint w-5">{i+1}</span>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm truncate">{item.ten}</div>
                        <div className="w-full bg-surface-muted rounded-full h-1.5 mt-1">
                          <div
                            className="bg-primary h-1.5 rounded-full"
                            style={{ width: `${(item.luot_muon / (top[0]?.luot_muon||1))*100}%` }}
                          />
                        </div>
                      </div>
                      <span className="text-xs font-medium text-ink-muted">{item.luot_muon}</span>
                    </div>
                  ))}
                </div>
            }
          </div>
        </div>
      </div>
    </div>
  )
}
