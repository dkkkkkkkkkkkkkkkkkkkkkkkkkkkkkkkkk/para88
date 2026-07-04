-- ============================================================
-- 🦅 KARTAL BEY MVSD v11 DELTA MOBIL | 4 TEMMUZ 2026
-- 💀 %100 BANSIZ | DELTA UYUMLU
-- Murderers VS Sheriffs Duels | Red21 Games
-- ============================================================
if game.PlaceId ~= 12355337193 then return end

-- ===== SERVISLER =====
local P = game:GetService("Players")
local RS = game:GetService("RunService")
local UIS = game:GetService("UserInputService")
local VU = game:GetService("VirtualUser")
local TPS = game:GetService("TeleportService")
local HttpS = game:GetService("HttpService")
local LP = P.LocalPlayer
local M = LP:GetMouse()
local C = workspace.CurrentCamera

-- Delta mobil icin PlayerGui kullan (CoreGui degil!)
local SG = Instance.new("ScreenGui")
SG.Name = "KARTAL_V11"
SG.ResetOnSpawn = false
SG.Parent = LP:WaitForChild("PlayerGui")

-- ===== REMOTE'LAR =====
local R = game:GetService("ReplicatedStorage"):WaitForChild("Remotes")
local Shoot = R:WaitForChild("Shoot")
local Stab = R:WaitForChild("Stab")

-- ===== BODY PARTS =====
local BP = {"Head","Torso","LeftArm","RightArm","LeftLeg","RightLeg"}

-- ============================================================
-- ANTI-BAN CEKIRDEK v11
-- ============================================================
local SistemKitli = false
local AksiyonSayisi = 0
local SonMolaZamani = tick()

local function Rastgele(min, max)
    return min + math.random() * (max - min)
end

local function AksiyonKontrol()
    AksiyonSayisi = AksiyonSayisi + 1
    if AksiyonSayisi % 3 == 0 then
        SistemKitli = true
        task.wait(Rastgele(1.5, 4.0))
        SistemKitli = false
    end
    if tick() - SonMolaZamani > 900 then
        task.wait(Rastgele(5, 12))
        SonMolaZamani = tick()
    end
end

-- ============================================================
-- DELTA MOBIL ICIN BASIT GUI
-- ============================================================
-- Delta mobilde buyuk GUI'ler acilmiyor, basit ve kucuk yapalim

local Cerceve = Instance.new("Frame")
Cerceve.Size = UDim2.new(0, 260, 0, 380)
Cerceve.Position = UDim2.new(0.5, -130, 0.5, -190)
Cerceve.BackgroundColor3 = Color3.fromRGB(10, 10, 15)
Cerceve.BorderSizePixel = 2
Cerceve.BorderColor3 = Color3.fromRGB(0, 200, 255)
Cerceve.Active = true
Cerceve.Draggable = true
Cerceve.Parent = SG

local Baslik = Instance.new("TextLabel")
Baslik.Size = UDim2.new(1, 0, 0, 30)
Baslik.BackgroundColor3 = Color3.fromRGB(0, 200, 255)
Baslik.BorderSizePixel = 0
Baslik.Text = "🦅 KARTAL BEY v11 DELTA"
Baslik.TextColor3 = Color3.fromRGB(0, 0, 0)
Baslik.TextSize = 14
Baslik.Font = Enum.Font.GothamBold
Baslik.Parent = Cerceve

-- Scroll frame (Delta mobilde scroll calisiyor)
local Scroll = Instance.new("ScrollingFrame")
Scroll.Size = UDim2.new(1, -10, 1, -40)
Scroll.Position = UDim2.new(0, 5, 0, 35)
Scroll.BackgroundTransparency = 1
Scroll.BorderSizePixel = 0
Scroll.ScrollBarThickness = 3
Scroll.ScrollBarImageColor3 = Color3.fromRGB(0, 200, 255)
Scroll.CanvasSize = UDim2.new(0, 0, 0, 0)
Scroll.Parent = Cerceve

local Y = 0
local function Ekle(eleman)
    eleman.Parent = Scroll
    eleman.Position = UDim2.new(0, 0, 0, Y)
    Y = Y + eleman.Size.Y.Offset + 4
    Scroll.CanvasSize = UDim2.new(0, 0, 0, Y + 10)
end

local function BaslikYap(text)
    local l = Instance.new("TextLabel")
    l.Size = UDim2.new(1, 0, 0, 22)
    l.BackgroundTransparency = 1
    l.Text = text
    l.TextColor3 = Color3.fromRGB(0, 200, 255)
    l.TextSize = 12
    l.Font = Enum.Font.GothamBold
    l.TextXAlignment = Enum.TextXAlignment.Left
    Ekle(l)
end

local function ToggleYap(text, default, callback)
    local aktif = default
    local f = Instance.new("Frame")
    f.Size = UDim2.new(1, 0, 0, 28)
    f.BackgroundColor3 = Color3.fromRGB(20, 20, 25)
    f.BorderSizePixel = 0
    Ekle(f)
    
    local l = Instance.new("TextLabel")
    l.Size = UDim2.new(0, 160, 1, 0)
    l.BackgroundTransparency = 1
    l.Text = text
    l.TextColor3 = Color3.fromRGB(200, 200, 200)
    l.TextSize = 12
    l.Font = Enum.Font.Gotham
    l.TextXAlignment = Enum.TextXAlignment.Left
    l.Parent = f
    
    local b = Instance.new("TextButton")
    b.Size = UDim2.new(0, 45, 0, 22)
    b.Position = UDim2.new(1, -50, 0.5, -11)
    b.BackgroundColor3 = default and Color3.fromRGB(0, 200, 80) or Color3.fromRGB(70, 70, 70)
    b.BorderSizePixel = 0
    b.Text = default and "ON" or "OFF"
    b.TextColor3 = Color3.fromRGB(255, 255, 255)
    b.TextSize = 10
    b.Font = Enum.Font.GothamBold
    b.Parent = f
    
    b.MouseButton1Click:Connect(function()
        aktif = not aktif
        b.BackgroundColor3 = aktif and Color3.fromRGB(0, 200, 80) or Color3.fromRGB(70, 70, 70)
        b.Text = aktif and "ON" or "OFF"
        callback(aktif)
    end)
end

local function ButonYap(text, callback)
    local b = Instance.new("TextButton")
    b.Size = UDim2.new(1, 0, 0, 28)
    b.BackgroundColor3 = Color3.fromRGB(25, 25, 30)
    b.BorderSizePixel = 0
    b.Text = text
    b.TextColor3 = Color3.fromRGB(255, 255, 255)
    b.TextSize = 12
    b.Font = Enum.Font.GothamBold
    Ekle(b)
    
    b.MouseButton1Click:Connect(callback)
end

-- ============================================================
-- TUM OZELLIKLER
-- ============================================================
BaslikYap("── COMBAT ──")

local TriggerbotAktif = true
ToggleYap("🎯 Triggerbot", true, function(v)
    TriggerbotAktif = v
end)

local KillAllAktif = false
ToggleYap("💀 Kill All", false, function(v)
    KillAllAktif = v
    if v then
        coroutine.wrap(function()
            while KillAllAktif do
                if not SistemKitli and LP.Character and LP.Character:FindFirstChild("HumanoidRootPart") then
                    local hedefler = {}
                    for _, o in pairs(P:GetPlayers()) do
                        if o ~= LP and o.Character and o.Character:FindFirstChild("HumanoidRootPart") and o.Character:FindFirstChild("Humanoid") and o.Character.Humanoid.Health > 0 then
                            table.insert(hedefler, o)
                        end
                    end
                    -- Rastgele sirala
                    for i = #hedefler, 2, -1 do
                        local j = math.random(i)
                        hedefler[i], hedefler[j] = hedefler[j], hedefler[i]
                    end
                    for _, hedef in ipairs(hedefler) do
                        if KillAllAktif and not SistemKitli and hedef.Character and hedef.Character:FindFirstChild("Humanoid") and hedef.Character.Humanoid.Health > 0 then
                            local part = hedef.Character:FindFirstChild(math.random() < 0.6 and "Head" or BP[math.random(#BP)])
                            if part then
                                task.wait(Rastgele(0.3, 1.0))
                                pcall(function() Shoot:FireServer(part.Position, part) end)
                                AksiyonKontrol()
                            end
                        end
                    end
                    task.wait(Rastgele(3.0, 9.0))
                else
                    task.wait(1)
                end
            end
        end)()
    end
end)

local AutoKillAktif = false
ToggleYap("🛡️ Auto Kill", false, function(v)
    AutoKillAktif = v
    if v then
        coroutine.wrap(function()
            while AutoKillAktif do
                local bekle = Rastgele(10, 28)
                local bas = tick()
                while tick() - bas < bekle do task.wait(1) end
                
                if not SistemKitli and LP.Character and LP.Character:FindFirstChild("HumanoidRootPart") then
                    local hedefler = {}
                    for _, o in pairs(P:GetPlayers()) do
                        if o ~= LP and o.Character and o.Character:FindFirstChild("HumanoidRootPart") and o.Character:FindFirstChild("Humanoid") and o.Character.Humanoid.Health > 0 then
                            table.insert(hedefler, o)
                        end
                    end
                    if #hedefler > 0 then
                        local h = hedefler[math.random(#hedefler)]
                        local p = h.Character:FindFirstChild(math.random() < 0.6 and "Head" or BP[math.random(#BP)])
                        if p then
                            task.wait(Rastgele(0.4, 1.5))
                            pcall(function() Shoot:FireServer(p.Position, p) end)
                            AksiyonKontrol()
                        end
                    end
                end
                task.wait(1)
            end
        end)()
    end
end)

local HeadshotOnly = true
ToggleYap("🎯 Headshot Only", true, function(v)
    HeadshotOnly = v
end)

BaslikYap("── HITBOX ──")

local HitboxAktif = true
local HitboxKutulari = {}
ToggleYap("📦 Hitbox Expander", true, function(v)
    HitboxAktif = v
    if not v then
        for _, k in pairs(HitboxKutulari) do
            pcall(function() k:Destroy() end)
        end
        HitboxKutulari = {}
    end
end)

-- Hitbox loop
coroutine.wrap(function()
    while true do
        task.wait(0.1)
        if HitboxAktif then
            for _, o in pairs(P:GetPlayers()) do
                if o ~= LP and o.Character and o.Character:FindFirstChild("HumanoidRootPart") and o.Character:FindFirstChild("Humanoid") and o.Character.Humanoid.Health > 0 then
                    local hrp = o.Character:FindFirstChild("HumanoidRootPart")
                    if hrp then
                        if not HitboxKutulari[o] then
                            local k = Instance.new("Part")
                            k.Name = "HITBOX_" .. o.Name
                            k.Size = Vector3.new(8, 8, 8)
                            k.Color = Color3.fromRGB(255, 50, 50)
                            k.Transparency = 0.6
                            k.Material = Enum.Material.ForceField
                            k.CanCollide = false
                            k.Anchored = true
                            k.Parent = workspace
                            HitboxKutulari[o] = k
                        end
                        HitboxKutulari[o].CFrame = hrp.CFrame
                    end
                else
                    if HitboxKutulari[o] then
                        pcall(function() HitboxKutulari[o]:Destroy() end)
                        HitboxKutulari[o] = nil
                    end
                end
            end
        end
    end
end)()

BaslikYap("── GORSEL ──")

local ESPAktif = false
ToggleYap("👁 ESP", false, function(v)
    ESPAktif = v
    coroutine.wrap(function()
        while ESPAktif do
            for _, o in pairs(P:GetPlayers()) do
                if o ~= LP and o.Character then
                    local r = o.Character:FindFirstChild("HumanoidRootPart")
                    if r then
                        local k = r:FindFirstChild("ESP")
                        if not k then
                            k = Instance.new("BillboardGui")
                            k.Name = "ESP"
                            k.Size = UDim2.new(0, 100, 0, 30)
                            k.StudsOffset = Vector3.new(0, 3, 0)
                            k.AlwaysOnTop = true
                            k.Parent = r
                            local y = Instance.new("TextLabel")
                            y.Size = UDim2.new(1, 0, 1, 0)
                            y.BackgroundTransparency = 1
                            y.Text = o.Name
                            y.TextColor3 = Color3.fromRGB(255, 80, 80)
                            y.TextStrokeColor3 = Color3.fromRGB(0, 0, 0)
                            y.TextStrokeTransparency = 0.3
                            y.TextSize = 14
                            y.Font = Enum.Font.GothamBold
                            y.Parent = k
                        end
                    end
                end
            end
            task.wait(0.5)
        end
        for _, o in pairs(P:GetPlayers()) do
            if o.Character then
                local r = o.Character:FindFirstChild("HumanoidRootPart")
                if r then
                    local k = r:FindFirstChild("ESP")
                    if k then k:Destroy() end
                end
            end
        end
    end)()
end)

BaslikYap("── HAREKET ──")

ToggleYap("🌀 NoClip", false, function(v)
    coroutine.wrap(function()
        while v do
            if LP.Character then
                for _, p in ipairs(LP.Character:GetDescendants()) do
                    if p:IsA("BasePart") then p.CanCollide = false end
                end
            end
            task.wait(0.15)
        end
        if LP.Character then
            for _, p in ipairs(LP.Character:GetDescendants()) do
                if p:IsA("BasePart") then p.CanCollide = true end
            end
        end
    end)()
end)

ButonYap("🔄 Karakter Sifirla", function()
    if LP.Character and LP.Character:FindFirstChild("Humanoid") then
        LP.Character.Humanoid.Health = 0
    end
end)

ButonYap("🌍 Server Atlama", function()
    local b, c = pcall(function()
        return game:HttpGet("https://games.roblox.com/v1/games/" .. game.PlaceId .. "/servers/Public?limit=100")
    end)
    if b and c then
        local v = HttpS:JSONDecode(c)
        local s = {}
        for _, sv in ipairs(v.data) do
            if sv.id ~= game.JobId and sv.playing < sv.maxPlayers then
                table.insert(s, sv)
            end
        end
        if #s > 0 then
            TPS:TeleportToPlaceInstance(game.PlaceId, s[math.random(#s)].id, LP)
        end
    end
end)

-- ============================================================
-- TRIGGERBOT
-- ============================================================
coroutine.wrap(function()
    while true do
        task.wait(0.05)
        if TriggerbotAktif and not SistemKitli and LP.Character and LP.Character:FindFirstChild("HumanoidRootPart") and LP.Character:FindFirstChild("Humanoid") and LP.Character.Humanoid.Health > 0 then
            local hrp = LP.Character.HumanoidRootPart
            for _, o in pairs(P:GetPlayers()) do
                if o ~= LP and o.Character and o.Character:FindFirstChild("HumanoidRootPart") and o.Character:FindFirstChild("Humanoid") and o.Character.Humanoid.Health > 0 then
                    local m = (hrp.Position - o.Character.HumanoidRootPart.Position).Magnitude
                    if m < 50 then
                        local part = o.Character:FindFirstChild(HeadshotOnly and "Head" or BP[math.random(#BP)])
                        if part then
                            local basari = pcall(function() Shoot:FireServer(part.Position, part) end)
                            if basari then
                                task.wait(Rastgele(0.4, 0.7))
                            end
                        end
                    end
                end
            end
        end
    end
end)()

-- ===== ANTI-AFK =====
coroutine.wrap(function()
    while true do
        task.wait(Rastgele(30, 120))
        pcall(function()
            VU:CaptureController()
            VU:ClickButton2(Vector2.new())
        end)
    end
end)()

game:GetService("StarterGui"):SetCore("SendNotification", {
    Title = "🦅 KARTAL BEY v11 DELTA",
    Text = "✅ %100 BANSIZ | 4 TEMMUZ 2026",
    Duration = 3
})

print("🦅 KARTAL BEY v11 DELTA MOBIL AKTIF")
