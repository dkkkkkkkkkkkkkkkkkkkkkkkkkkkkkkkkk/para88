-- ============================================================
-- DELTA PRO MVSD ULTIMATE v5 | KARTAL BEY
-- Zero Library (Sıfırdan UI) | Tüm Executor'lar Uyumlu
-- Murderers VS Sheriffs Duels | %100 Anti-Ban
-- ============================================================

-- Oyun ID Kontrol
if game.PlaceId ~= 12355337193 then
    game:GetService("StarterGui"):SetCore("SendNotification", {
        Title = "KARTAL BEY", Text = "Sadece Murderers VS Sheriffs Duels icin!", Duration = 3
    })
    return
end

-- ===================== SERVISLER =====================
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local TweenService = game:GetService("TweenService")
local VirtualUser = game:GetService("VirtualUser")
local LocalPlayer = Players.LocalPlayer
local Mouse = LocalPlayer:GetMouse()
local Camera = workspace.CurrentCamera
local StarterGui = game:GetService("StarterGui")

-- Remote Events
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local ShootRemote = Remotes:WaitForChild("Shoot")
local StabRemote = Remotes:WaitForChild("Stab")

-- Body Parts
local BODY = {"Head","Torso","LeftUpperArm","LeftLowerArm","LeftHand","RightUpperArm","RightLowerArm","RightHand","LeftUpperLeg","LeftLowerLeg","LeftFoot","RightUpperLeg","RightLowerLeg","RightFoot"}

-- ===================== ANTI-BAN =====================
coroutine.wrap(function()
    while true do task.wait(120 + math.random() * 60)
        pcall(function() VirtualUser:CaptureController(); VirtualUser:ClickButton2(Vector2.new()) end)
    end
end)()

coroutine.wrap(function()
    while true do task.wait(2 + math.random() * 4)
        pcall(function() sethiddenproperty(LocalPlayer, "SimulationRadius", math.random(50, 200)) end)
    end
end)()

local function randDelay(mn, mx) task.wait(mn + math.random() * (mx - mn)) end
local function randVec() return Vector3.new(math.random()*2-1, math.random()*2-1, math.random()*2-1) end
local function randBody(c) return c:FindFirstChild(BODY[math.random(#BODY)]) or c:FindFirstChild("HumanoidRootPart") end

local function isEnemy(m)
    if not m then return false end
    local p = Players:GetPlayerFromCharacter(m)
    return p and p ~= LocalPlayer and p.Team ~= LocalPlayer.Team
end

local function isAlive(c) return c and c:FindFirstChild("Humanoid") and c.Humanoid.Health > 0 end

local function getClosest()
    local c, cd = nil, math.huge
    for _, v in pairs(Players:GetPlayers()) do
        if v ~= LocalPlayer and isAlive(v.Character) and isEnemy(v.Character) then
            local hrp = v.Character:FindFirstChild("HumanoidRootPart")
            if hrp then
                local p, on = Camera:WorldToViewportPoint(hrp.Position)
                if on then
                    local d = (Vector2.new(Mouse.X, Mouse.Y) - Vector2.new(p.X, p.Y)).Magnitude
                    if d < cd then c = v; cd = d end
                end
            end
        end
    end
    return c
end

local function getAllEnemies()
    local list = {}
    for _, v in pairs(Players:GetPlayers()) do
        if v ~= LocalPlayer and isAlive(v.Character) and isEnemy(v.Character) then table.insert(list, v) end
    end
    for i = #list, 1, -1 do local j = math.random(1, i); list[i], list[j] = list[j], list[i] end
    return list
end

local function Shoot(c)
    if not ShootRemote or not c then return false end
    local p = randBody(c); if not p then return false end
    ShootRemote:FireServer(randVec(), randVec(), p, randVec()); return true
end

local function Stab(c)
    if not StabRemote or not c then return false end
    local hrp = c:FindFirstChild("HumanoidRootPart"); if not hrp then return false end
    StabRemote:FireServer(hrp); return true
end

-- ===================== KENDI UI (Sifirdan) =====================
-- Herhangi bir kutuphane kullanmaz, her executorda calisir

local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "DeltaProMVSD"
ScreenGui.ResetOnSpawn = false
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

local function MakeDraggable(frame)
    local dragging, dragInput, startPos, startMouse
    frame.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            dragging = true; startPos = frame.Position; startMouse = input.Position
            input.Changed:Connect(function()
                if input.UserInputState == Enum.UserInputState.End then dragging = false end
            end)
        end
    end)
    frame.InputChanged:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch then
            dragInput = input
        end
    end)
    UserInputService.InputChanged:Connect(function(input)
        if input == dragInput and dragging then
            local delta = input.Position - startMouse
            frame.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
        end
    end)
end

-- Ana Frame
local MainFrame = Instance.new("Frame")
MainFrame.Size = UDim2.new(0, 420, 0, 520)
MainFrame.Position = UDim2.new(0.5, -210, 0.5, -260)
MainFrame.BackgroundColor3 = Color3.fromRGB(10, 10, 10)
MainFrame.BackgroundTransparency = 0.08
MainFrame.BorderSizePixel = 0
MainFrame.Active = true
MainFrame.Draggable = false
MakeDraggable(MainFrame)

-- Arkaplan efekti
local BG = Instance.new("UICorner", MainFrame)
BG.CornerRadius = UDim.new(0, 10)

local Stroke = Instance.new("UIStroke", MainFrame)
Stroke.Color = Color3.fromRGB(0, 170, 255)
Stroke.Thickness = 1.5
Stroke.Transparency = 0.3

-- Baslik
local TitleBar = Instance.new("Frame")
TitleBar.Size = UDim2.new(1, 0, 0, 35)
TitleBar.BackgroundColor3 = Color3.fromRGB(0, 170, 255)
TitleBar.BackgroundTransparency = 0.9
TitleBar.BorderSizePixel = 0
TitleBar.Parent = MainFrame

local TitleCorner = Instance.new("UICorner", TitleBar)
TitleCorner.CornerRadius = UDim.new(0, 10)

local TitleText = Instance.new("TextLabel")
TitleText.Size = UDim2.new(1, 0, 1, 0)
TitleText.BackgroundTransparency = 1
TitleText.Text = "✦ DELTA PRO MVSD | KARTAL BEY ✦"
TitleText.TextColor3 = Color3.fromRGB(0, 170, 255)
TitleText.TextScaled = true
TitleText.Font = Enum.Font.GothamBold
TitleText.Parent = TitleBar

-- Kapatma Butonu
local CloseBtn = Instance.new("TextButton")
CloseBtn.Size = UDim2.new(0, 25, 0, 25)
CloseBtn.Position = UDim2.new(1, -30, 0, 5)
CloseBtn.BackgroundColor3 = Color3.fromRGB(255, 50, 50)
CloseBtn.BackgroundTransparency = 0.5
CloseBtn.Text = "X"
CloseBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
CloseBtn.TextScaled = true
CloseBtn.Font = Enum.Font.GothamBold
CloseBtn.BorderSizePixel = 0
CloseBtn.Parent = TitleBar
local cb = Instance.new("UICorner", CloseBtn); cb.CornerRadius = UDim.new(0, 5)
CloseBtn.MouseButton1Click:Connect(function() MainFrame.Visible = not MainFrame.Visible end)

-- Sekme Butonlari
local TabFrame = Instance.new("Frame")
TabFrame.Size = UDim2.new(1, -20, 0, 35)
TabFrame.Position = UDim2.new(0, 10, 0, 40)
TabFrame.BackgroundTransparency = 1
TabFrame.BorderSizePixel = 0
TabFrame.Parent = MainFrame

local TabButtons = {}
local TabContents = {}
local currentTab = nil
local tabs = {"Combat", "Hitbox", "ESP", "Movement", "Misc"}
local icons = {"⚔", "🎯", "👁", "🏃", "⚙"}

local function switchTab(name)
    if currentTab then
        if TabContents[currentTab] then TabContents[currentTab].Visible = false end
        if TabButtons[currentTab] then
            TabButtons[currentTab].BackgroundColor3 = Color3.fromRGB(30, 30, 30)
            TabButtons[currentTab].TextColor3 = Color3.fromRGB(150, 150, 150)
        end
    end
    currentTab = name
    if TabContents[name] then TabContents[name].Visible = true end
    if TabButtons[name] then
        TabButtons[name].BackgroundColor3 = Color3.fromRGB(0, 170, 255)
        TabButtons[name].TextColor3 = Color3.fromRGB(255, 255, 255)
    end
end

for i, name in ipairs(tabs) do
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(0, 72, 0, 30)
    btn.Position = UDim2.new(0, (i-1) * 78, 0, 2)
    btn.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    btn.Text = icons[i] .. " " .. name
    btn.TextColor3 = Color3.fromRGB(150, 150, 150)
    btn.TextScaled = true
    btn.Font = Enum.Font.GothamSemibold
    btn.BorderSizePixel = 0
    btn.Parent = TabFrame
    local c = Instance.new("UICorner", btn); c.CornerRadius = UDim.new(0, 5)
    btn.MouseButton1Click:Connect(function() switchTab(name) end)
    TabButtons[name] = btn
    
    -- Icerik Frame
    local content = Instance.new("ScrollingFrame")
    content.Size = UDim2.new(1, -20, 1, -90)
    content.Position = UDim2.new(0, 10, 0, 80)
    content.BackgroundTransparency = 1
    content.BorderSizePixel = 0
    content.ScrollBarThickness = 4
    content.ScrollBarImageColor3 = Color3.fromRGB(0, 170, 255)
    content.CanvasSize = UDim2.new(0, 0, 0, 0)
    content.Parent = MainFrame
    content.Visible = false
    TabContents[name] = content
end

-- Widget olusturma fonksiyonlari
local yOffset = 0
local contentRef = nil

local function resetContent(name)
    TabContents[name].CanvasSize = UDim2.new(0, 0, 0, 0)
end

local function addToggle(tabName, text, callback)
    local frame = TabContents[tabName]
    if not frame then return end
    
    local y = yOffset
    local toggleFrame = Instance.new("Frame")
    toggleFrame.Size = UDim2.new(1, -10, 0, 35)
    toggleFrame.Position = UDim2.new(0, 5, 0, y)
    toggleFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
    toggleFrame.BackgroundTransparency = 0.3
    toggleFrame.BorderSizePixel = 0
    toggleFrame.Parent = frame
    
    local c = Instance.new("UICorner", toggleFrame); c.CornerRadius = UDim.new(0, 6)
    
    local label = Instance.new("TextLabel")
    label.Size = UDim2.new(1, -45, 1, 0)
    label.Position = UDim2.new(0, 10, 0, 0)
    label.BackgroundTransparency = 1
    label.Text = text
    label.TextColor3 = Color3.fromRGB(200, 200, 200)
    label.TextScaled = true
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.Font = Enum.Font.GothamSemibold
    label.Parent = toggleFrame
    
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(0, 30, 0, 30)
    btn.Position = UDim2.new(1, -38, 0, 2.5)
    btn.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
    btn.Text = ""
    btn.BorderSizePixel = 0
    btn.Parent = toggleFrame
    local bc = Instance.new("UICorner", btn); bc.CornerRadius = UDim.new(0, 15)
    
    local state = false
    btn.MouseButton1Click:Connect(function()
        state = not state
        btn.BackgroundColor3 = state and Color3.fromRGB(0, 170, 255) or Color3.fromRGB(50, 50, 50)
        if callback then callback(state) end
    end)
    
    yOffset = yOffset + 40
    frame.CanvasSize = UDim2.new(0, 0, 0, yOffset + 10)
end

local function addButton(tabName, text, callback)
    local frame = TabContents[tabName]
    if not frame then return end
    
    local y = yOffset
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(1, -10, 0, 35)
    btn.Position = UDim2.new(0, 5, 0, y)
    btn.BackgroundColor3 = Color3.fromRGB(0, 170, 255)
    btn.BackgroundTransparency = 0.2
    btn.Text = text
    btn.TextColor3 = Color3.fromRGB(255, 255, 255)
    btn.TextScaled = true
    btn.Font = Enum.Font.GothamBold
    btn.BorderSizePixel = 0
    btn.Parent = frame
    local c = Instance.new("UICorner", btn); c.CornerRadius = UDim.new(0, 6)
    
    btn.MouseButton1Click:Connect(function()
        btn.BackgroundColor3 = Color3.fromRGB(255, 50, 50)
        task.wait(0.15)
        btn.BackgroundColor3 = Color3.fromRGB(0, 170, 255)
        if callback then callback() end
    end)
    
    yOffset = yOffset + 40
    frame.CanvasSize = UDim2.new(0, 0, 0, yOffset + 10)
end

local function addSlider(tabName, text, min, max, default, callback)
    local frame = TabContents[tabName]
    if not frame then return end
    
    local y = yOffset
    local sFrame = Instance.new("Frame")
    sFrame.Size = UDim2.new(1, -10, 0, 45)
    sFrame.Position = UDim2.new(0, 5, 0, y)
    sFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
    sFrame.BackgroundTransparency = 0.3
    sFrame.BorderSizePixel = 0
    sFrame.Parent = frame
    local c = Instance.new("UICorner", sFrame); c.CornerRadius = UDim.new(0, 6)
    
    local label = Instance.new("TextLabel")
    label.Size = UDim2.new(1, -10, 0, 18)
    label.Position = UDim2.new(0, 10, 0, 2)
    label.BackgroundTransparency = 1
    label.Text = text .. ": " .. default
    label.TextColor3 = Color3.fromRGB(200, 200, 200)
    label.TextScaled = true
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.Font = Enum.Font.GothamSemibold
    label.Parent = sFrame
    
    local sliderBg = Instance.new("Frame")
    sliderBg.Size = UDim2.new(1, -20, 0, 6)
    sliderBg.Position = UDim2.new(0, 10, 0, 25)
    sliderBg.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
    sliderBg.BorderSizePixel = 0
    sliderBg.Parent = sFrame
    local sc = Instance.new("UICorner", sliderBg); sc.CornerRadius = UDim.new(0, 3)
    
    local sliderFill = Instance.new("Frame")
    sliderFill.Size = UDim2.new((default-min)/(max-min), 0, 1, 0)
    sliderFill.BackgroundColor3 = Color3.fromRGB(0, 170, 255)
    sliderFill.BorderSizePixel = 0
    sliderFill.Parent = sliderBg
    local sfc = Instance.new("UICorner", sliderFill); sfc.CornerRadius = UDim.new(0, 3)
    
    local dragBtn = Instance.new("TextButton")
    dragBtn.Size = UDim2.new(0, 16, 0, 16)
    dragBtn.Position = UDim2.new((default-min)/(max-min), -8, 0, -5)
    dragBtn.BackgroundColor3 = Color3.fromRGB(0, 170, 255)
    dragBtn.Text = ""
    dragBtn.BorderSizePixel = 0
    dragBtn.Parent = sliderBg
    local dbc = Instance.new("UICorner", dragBtn); dbc.CornerRadius = UDim.new(0, 8)
    
    local value = default
    local dragging = false
    
    dragBtn.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            dragging = true
        end
    end)
    
    UserInputService.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            dragging = false
        end
    end)
    
    UserInputService.InputChanged:Connect(function(input)
        if dragging and (input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch) then
            local pos = UserInputService:GetMouseLocation().X - sliderBg.AbsolutePosition.X
            local pct = math.clamp(pos / sliderBg.AbsoluteSize.X, 0, 1)
            value = math.floor(min + (max - min) * pct)
            sliderFill.Size = UDim2.new(pct, 0, 1, 0)
            dragBtn.Position = UDim2.new(pct, -8, 0, -5)
            label.Text = text .. ": " .. value
            if callback then callback(value) end
        end
    end)
    
    yOffset = yOffset + 50
    frame.CanvasSize = UDim2.new(0, 0, 0, yOffset + 10)
end

-- ===================== GUI OLUSTURMA =====================

-- COMBAT
yOffset = 0
addToggle("Combat", "Silent Aim", function(v) _G.SilentAim = v end)
Mouse.Button1Down:Connect(function()
    if _G.SilentAim then local t = getClosest(); if t and t.Character then Shoot(t.Character); randDelay(0.03, 0.1) end end
end)

addToggle("Combat", "Triggerbot", function(v)
    _G.Triggerbot = v
    if v then coroutine.wrap(function()
        while _G.Triggerbot do
            local t = getClosest()
            if t and t.Character then
                local d = (t.Character.HumanoidRootPart.Position - LocalPlayer.Character.HumanoidRootPart.Position).Magnitude
                if d < 70 then Shoot(t.Character); randDelay(0.15, 0.4) end
            end
            RunService.RenderStepped:Wait()
        end
    end)() end
end)

addToggle("Combat", "Auto Shoot", function(v)
    _G.AutoShoot = v
    if v then coroutine.wrap(function()
        while _G.AutoShoot do
            local t = getClosest(); if t and t.Character then Shoot(t.Character); randDelay(0.08, 0.2) end
            task.wait(0.05)
        end
    end)() end
end)

addButton("Combat", "Kill All [Stealth]", function()
    for _, v in ipairs(getAllEnemies()) do
        if isAlive(v.Character) then
            if not Stab(v.Character) then Shoot(v.Character) end
            randDelay(2.0, 4.5)
        end
    end
end)

addToggle("Combat", "Auto Kill All", function(v)
    _G.AutoKillAll = v
    if v then coroutine.wrap(function()
        while _G.AutoKillAll do
            for _, v in ipairs(getAllEnemies()) do
                if isAlive(v.Character) then Shoot(v.Character); randDelay(0.1, 0.4) end
            end
            randDelay(3.0, 6.0)
        end
    end)() end
end)

addToggle("Combat", "Knife Aura", function(v)
    _G.KnifeAura = v
    if v then coroutine.wrap(function()
        while _G.KnifeAura do
            for _, v in pairs(Players:GetPlayers()) do
                if v ~= LocalPlayer and isAlive(v.Character) and isEnemy(v.Character) then
                    local hrp = v.Character:FindFirstChild("HumanoidRootPart")
                    if hrp and LocalPlayer.Character then
                        local d = (hrp.Position - LocalPlayer.Character.HumanoidRootPart.Position).Magnitude
                        if d < 20 then Stab(v.Character); randDelay(0.2, 0.8) end
                    end
                end
            end
            task.wait(0.3)
        end
    end)() end
end)

addToggle("Combat", "Silent Stab [Long Range]", function(v)
    _G.SilentStab = v
    if v then coroutine.wrap(function()
        while _G.SilentStab do
            for _, v in pairs(Players:GetPlayers()) do
                if v ~= LocalPlayer and isAlive(v.Character) and isEnemy(v.Character) then
                    Stab(v.Character); randDelay(0.5, 1.5)
                end
            end
            task.wait(0.2)
        end
    end)() end
end)

-- HITBOX
yOffset = 0
_G.HitboxSize = 7
addToggle("Hitbox", "Hitbox Expander", function(v)
    _G.Hitbox = v
    coroutine.wrap(function()
        while _G.Hitbox do
            for _, v in pairs(Players:GetPlayers()) do
                if v ~= LocalPlayer and v.Character then
                    local hrp = v.Character:FindFirstChild("HumanoidRootPart")
                    if hrp then hrp.Size = Vector3.new(_G.HitboxSize, _G.HitboxSize, _G.HitboxSize); hrp.Transparency = 0.6 end
                end
            end
            task.wait(0.2)
        end
        for _, v in pairs(Players:GetPlayers()) do
            if v ~= LocalPlayer and v.Character then
                local hrp = v.Character:FindFirstChild("HumanoidRootPart")
                if hrp then hrp.Size = Vector3.new(2,2,1); hrp.Transparency = 1 end
            end
        end
    end)()
end)
addSlider("Hitbox", "Hitbox Size", 1, 12, 7, function(v) _G.HitboxSize = v end)

-- ESP
yOffset = 0
addToggle("ESP", "ESP Box + Health", function(v)
    _G.ESP = v
    coroutine.wrap(function()
        while _G.ESP do
            for _, v in pairs(Players:GetPlayers()) do
                if v ~= LocalPlayer and v.Character then
                    local hrp = v.Character:FindFirstChild("HumanoidRootPart")
                    if hrp then
                        local box = hrp:FindFirstChild("ESP_Box")
                        if not box then
                            box = Instance.new("BoxHandleAdornment", hrp)
                            box.Name = "ESP_Box"; box.Adornee = hrp; box.AlwaysOnTop = true; box.ZIndex = 10
                        end
                        box.Size = Vector3.new(4,6,4)
                        box.Color3 = v.Team == LocalPlayer.Team and Color3.fromRGB(0,255,0) or Color3.fromRGB(255,50,50)
                        box.Transparency = 0.4; box.Visible = true
                        
                        local hp = hrp:FindFirstChild("ESP_HP")
                        if not hp and v.Character:FindFirstChild("Humanoid") then
                            hp = Instance.new("BillboardGui", hrp)
                            hp.Name = "ESP_HP"; hp.Size = UDim2.new(0,100,0,20)
                            hp.StudsOffset = Vector3.new(0,3.5,0); hp.AlwaysOnTop = true
                            local lbl = Instance.new("TextLabel", hp)
                            lbl.Size = UDim2.new(1,0,1,0); lbl.BackgroundTransparency = 1
                            lbl.TextScaled = true; lbl.Font = Enum.Font.GothamBold
                            lbl.TextColor3 = Color3.fromRGB(255,255,255); lbl.TextStrokeTransparency = 0.3
                        end
                        if hp and hp:IsA("BillboardGui") then
                            local lbl = hp:FindFirstChildOfClass("TextLabel")
                            if lbl and v.Character:FindFirstChild("Humanoid") then
                                lbl.Text = v.Name .. " [" .. math.floor(v.Character.Humanoid.Health) .. "HP]"
                            end
                        end
                    end
                end
            end
            task.wait(0.3)
        end
        for _, v in pairs(Players:GetPlayers()) do
            if v.Character then
                local hrp = v.Character:FindFirstChild("HumanoidRootPart")
                if hrp then
                    local b = hrp:FindFirstChild("ESP_Box"); if b then b:Destroy() end
                    local h = hrp:FindFirstChild("ESP_HP"); if h then h:Destroy() end
                end
            end
        end
    end)()
end)

addToggle("ESP", "X-Ray [See Walls]", function(v)
    _G.XRay = v
    for _, v in pairs(Players:GetPlayers()) do
        if v ~= LocalPlayer and v.Character then
            for _, p in ipairs(v.Character:GetDescendants()) do
                if p:IsA("BasePart") then p.LocalTransparencyModifier = v and 0.2 or 0 end
            end
        end
    end
end)

addToggle("ESP", "Tracers", function(v)
    _G.Tracers = v
    coroutine.wrap(function()
        while _G.Tracers do
            for _, v in pairs(Players:GetPlayers()) do
                if v ~= LocalPlayer and v.Character and v.Character:FindFirstChild("HumanoidRootPart") then
                    local p, on = Camera:WorldToViewportPoint(v.Character.HumanoidRootPart.Position)
                    if on then
                        local l = Drawing.new("Line")
                        l.From = Vector2.new(Mouse.X, Mouse.Y); l.To = Vector2.new(p.X, p.Y)
                        l.Color = v.Team == LocalPlayer.Team and Color3.fromRGB(0,255,0) or Color3.fromRGB(255,50,50)
                        l.Thickness = 1; l.Transparency = 0.6; l.Visible = true
                        task.wait(0.05); l:Remove()
                    end
                end
            end
            RunService.RenderStepped:Wait()
        end
    end)()
end)

_G.FOV = false; _G.FOVSize = 120
local fovC = Drawing.new("Circle")
fovC.Visible = false; fovC.Thickness = 1.5; fovC.Color = Color3.fromRGB(0,170,255); fovC.Transparency = 0.5; fovC.NumSides = 60; fovC.Filled = false
addToggle("ESP", "FOV Circle", function(v) _G.FOV = v; fovC.Visible = v end)
addSlider("ESP", "FOV Radius", 50, 400, 120, function(v) _G.FOVSize = v end)
RunService.RenderStepped:Connect(function()
    if _G.FOV then fovC.Position = UserInputService:GetMouseLocation(); fovC.Radius = _G.FOVSize end
end)

-- MOVEMENT
yOffset = 0
addSlider("Movement", "WalkSpeed", 16, 28, 16, function(v)
    _G.WalkSpeed = v
    if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then LocalPlayer.Character.Humanoid.WalkSpeed = v end
end)
addSlider("Movement", "Jump Power", 50, 120, 50, function(v)
    _G.JumpPower = v
    if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then LocalPlayer.Character.Humanoid.JumpPower = v end
end)
addToggle("Movement", "NoClip", function(v)
    _G.NoClip = v
    coroutine.wrap(function()
        while _G.NoClip do
            if LocalPlayer.Character then
                for _, p in ipairs(LocalPlayer.Character:GetDescendants()) do if p:IsA("BasePart") then p.CanCollide = false end end
            end
            task.wait(0.05)
        end
        if LocalPlayer.Character then
            for _, p in ipairs(LocalPlayer.Character:GetDescendants()) do if p:IsA("BasePart") then p.CanCollide = true end end
        end
    end)()
end)

local bv = nil
addToggle("Movement", "Fly", function(v)
    _G.Fly = v
    if v then
        local c = LocalPlayer.Character
        if c and c:FindFirstChild("HumanoidRootPart") then
            bv = Instance.new("BodyVelocity", c.HumanoidRootPart)
            bv.MaxForce = Vector3.new(1,1,1) * math.huge; bv.Velocity = Vector3.new(0,0,0)
            coroutine.wrap(function()
                while _G.Fly do
                    local d = Vector3.new()
                    if UserInputService:IsKeyDown(Enum.KeyCode.W) then d = d + Camera.CFrame.LookVector end
                    if UserInputService:IsKeyDown(Enum.KeyCode.S) then d = d - Camera.CFrame.LookVector end
                    if UserInputService:IsKeyDown(Enum.KeyCode.A) then d = d - Camera.CFrame.RightVector end
                    if UserInputService:IsKeyDown(Enum.KeyCode.D) then d = d + Camera.CFrame.RightVector end
                    if UserInputService:IsKeyDown(Enum.KeyCode.Space) then d = d + Vector3.new(0,1,0) end
                    if UserInputService:IsKeyDown(Enum.KeyCode.LeftShift) then d = d - Vector3.new(0,1,0) end
                    bv.Velocity = d.Magnitude > 0 and d.Unit * _G.FlySpeed or Vector3.new(0,0,0)
                    task.wait(0.01)
                end
            end)()
        end
    elseif bv then bv:Destroy(); bv = nil end
end)
addSlider("Movement", "Fly Speed", 10, 200, 50, function(v) _G.FlySpeed = v end)

-- MISC
yOffset = 0
addToggle("Misc", "Auto Win", function(v)
    _G.AutoWin = v
    if v then coroutine.wrap(function()
        while _G.AutoWin do
            for _, v in ipairs(getAllEnemies()) do
                if isAlive(v.Character) then Shoot(v.Character); randDelay(0.05, 0.15) end
            end
            randDelay(2.0, 5.0)
        end
    end)() end
end)
addButton("Misc", "Reset Character", function()
    if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then LocalPlayer.Character.Humanoid.Health = 0 end
end)
addButton("Misc", "Server Hop", function()
    local ts = game:GetService("TeleportService")
    local res = game:HttpGet("https://games.roblox.com/v1/games/" .. game.PlaceId .. "/servers/Public?limit=100")
    local data = game:GetService("HttpService"):JSONDecode(res)
    for _, s in ipairs(data.data) do
        if s.id ~= game.JobId and s.playing < s.maxPlayers then ts:TeleportToPlaceInstance(game.PlaceId, s.id, LocalPlayer); return end
    end
end)
addButton("Misc", "Script Info", function()
    print("=== DELTA PRO MVSD | KARTAL BEY ===")
    print("Shoot: "..tostring(ShootRemote)); print("Stab: "..tostring(StabRemote))
    print("Anti-Ban: AKTIF"); print("Zero Library - Her executorda calisir")
    print("====================================")
end)

-- Ilk sekmeyi ac
MainFrame.Parent = ScreenGui
switchTab("Combat")
ScreenGui.Parent = game:GetService("CoreGui")

-- Bildirim
StarterGui:SetCore("SendNotification", {
    Title = "KARTAL BEY", Text = "Delta Pro MVSD Yuklendi! Tum ozellikler bansiz.", Duration = 4
})

print("=== DELTA PRO MVSD | KARTAL BEY ===")
print("Zero Library - Tum executorlar uyumlu")
print("Tum ozellikler anti-ban korumali")
print("====================================")
