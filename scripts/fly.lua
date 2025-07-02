-- Fly Script (basic example)
local player = game.Players.LocalPlayer
local mouse = player:GetMouse()
local flying = false

mouse.KeyDown:Connect(function(key)
    if key == "f" then
        flying = not flying
        player.Character.HumanoidRootPart.Anchored = flying
    end
end)

