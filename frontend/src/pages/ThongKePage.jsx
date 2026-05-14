import { useEffect, useState } from 'react'
import { thongKeApi } from '../services/api'
import { PageHeader, Spinner, StatCard } from '../components/UI'
import { BookOpen, Users, Clock, AlertTriangle, CheckCircle } from 'lucide-react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  CartesianGrid, PieChart, Pie, Cell, Legend
} from 'recharts'

const COLORS = ['#1a56db','#057a55','#b45309','#c81e1e','#7c3aed','#0891b2']

export default function ThongKePage() {
  const [stats, setStats]   = useState(null)
  const [chart, setChart]   = useState([])
  const [top, setTop]       = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([thongKeApi.tongQuan(), thongKeApi.muonTheoThang(), thongKeApi.topTaiLieu()])
      .then(([s, c, t]) => { setStats(s.data); setChart(c.data); setTop(t.data) })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <Spinner />

  const pieData = top.slice(0, 6).map(t => ({ name: t.ten.slice(0, 25), value: t.luot_muon }))

  return (
    <div>
      <PageHeader title="Thống kê & Báo cáo" subtitle="Tổng hợp hoạt động thư viện" />
      <div className="px-6 space-y-6">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard label="Tổng tài liệu"      value={stats?.tong_tai_lieu?.toLocaleString()}     icon={BookOpen}     color="blue" />
          <StatCard label="Độc giả hoạt động"  value={stats?.doc_gia_hoat_dong?.toLocaleString()}  icon={Users}        color="green" />
          <StatCard label="Đang được mượn"     value={stats?.dang_duoc_muon?.toLocaleString()}     icon={CheckCircle} />
          <StatCard label="Vi phạm chưa xử lý" value={stats?.vi_pham_chua_xu_ly?.toLocaleString()} icon={AlertTriangle} color="red"
            sub={`${(stats?.tong_tien_phat_chua_thu||0).toLocaleString('vi-VN')}đ chưa thu`} />
        </div>

        <div className="grid lg:grid-cols-2 gap-4">
          <div className="card p-5">
            <h3 className="section-title">Lượt mượn theo tháng</h3>
            {chart.length === 0
              ? <p className="text-sm text-center text-ink-faint py-10">Chưa có dữ liệu</p>
              : <ResponsiveContainer width="100%" height={240}>
                  <BarChart data={chart} barSize={26}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="thang" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Bar dataKey="so_luong" fill="#1a56db" radius={[4,4,0,0]} name="Lượt mượn" />
                  </BarChart>
                </ResponsiveContainer>
            }
          </div>

          <div className="card p-5">
            <h3 className="section-title">Tỷ lệ tài liệu được mượn</h3>
            {pieData.length === 0
              ? <p className="text-sm text-center text-ink-faint py-10">Chưa có dữ liệu</p>
              : <ResponsiveContainer width="100%" height={240}>
                  <PieChart>
                    <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} label={({name,percent})=>`${(percent*100).toFixed(0)}%`}>
                      {pieData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                    </Pie>
                    <Tooltip />
                    <Legend iconSize={10} wrapperStyle={{ fontSize: 11 }} />
                  </PieChart>
                </ResponsiveContainer>
            }
          </div>
        </div>

        <div className="card p-5">
          <h3 className="section-title">Top 10 tài liệu được mượn nhiều nhất</h3>
          {top.length === 0
            ? <p className="text-sm text-center text-ink-faint py-8">Chưa có dữ liệu</p>
            : <div className="space-y-3">
                {top.map((item, i) => (
                  <div key={i} className="flex items-center gap-4">
                    <span className="w-6 text-center text-xs font-mono font-bold text-ink-faint">{i+1}</span>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium truncate mb-1">{item.ten}</div>
                      <div className="w-full bg-surface-muted rounded-full h-2">
                        <div className="h-2 rounded-full bg-primary transition-all"
                          style={{ width: `${(item.luot_muon / (top[0]?.luot_muon||1))*100}%` }} />
                      </div>
                    </div>
                    <span className="text-sm font-semibold text-ink w-12 text-right">{item.luot_muon}</span>
                  </div>
                ))}
              </div>
          }
        </div>
      </div>
    </div>
  )
}
