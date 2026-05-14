import { useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'

export default function UnauthorizedPage() {
  const { user } = useAuth()

  useEffect(() => {
    // Nếu đã có user token, redirect về dashboard
    if (user) {
      window.location.href = '/'
    }
  }, [user])

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-red-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md text-center">
        <div className="mb-6">
          <h1 className="text-6xl font-bold text-red-600 mb-2">❌</h1>
          <h2 className="text-3xl font-bold text-gray-800">Truy cập bị từ chối</h2>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
          <p className="text-gray-600 mb-4">
            Bạn cần xác thực để truy cập hệ thống quản lý thư viện.
          </p>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <p className="text-sm text-gray-700 mb-3">
              <strong>Hướng dẫn đăng nhập:</strong>
            </p>
            <code className="text-xs bg-gray-100 p-3 rounded block text-left mb-3 overflow-auto">
{`POST /api/auth/dang-nhap

{
  "email": "admin@thuvien.vn",
  "mat_khau": "18112006"
}`}
            </code>
            <p className="text-xs text-gray-600">
              Gửi request POST tới API endpoint trên để lấy token JWT, rồi đưa vào header:
            </p>
            <code className="text-xs bg-gray-100 p-2 rounded block text-left mt-2">
              Authorization: Bearer {'{token}'}</code>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-sm text-gray-700">
              <strong>⚠️ Lưu ý:</strong> Giao diện frontend chỉ hoạt động khi bạn đã đăng nhập thông qua API.
            </p>
            <p className="text-xs text-gray-600 mt-2">
              Nếu bạn là nhân viên thư viện, liên hệ quản trị viên để lấy tài khoản.
            </p>
          </div>
        </div>

        <button
          onClick={() => window.location.reload()}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
        >
          Thử lại
        </button>
      </div>
    </div>
  )
}
