/*
  Warnings:

  - You are about to drop the `AssetIsRequestBuy` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `AssetIsSell` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Assets` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Transaction` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "AssetIsRequestBuy" DROP CONSTRAINT "AssetIsRequestBuy_assetId_fkey";

-- DropForeignKey
ALTER TABLE "AssetIsRequestBuy" DROP CONSTRAINT "AssetIsRequestBuy_userId_fkey";

-- DropForeignKey
ALTER TABLE "AssetIsSell" DROP CONSTRAINT "AssetIsSell_assetId_fkey";

-- DropForeignKey
ALTER TABLE "AssetIsSell" DROP CONSTRAINT "AssetIsSell_userId_fkey";

-- DropForeignKey
ALTER TABLE "Assets" DROP CONSTRAINT "Assets_owner_id_fkey";

-- DropTable
DROP TABLE "AssetIsRequestBuy";

-- DropTable
DROP TABLE "AssetIsSell";

-- DropTable
DROP TABLE "Assets";

-- DropTable
DROP TABLE "Transaction";
